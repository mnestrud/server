"""
Byte-range support for single item streams.

A player that pauses on the device closes its connection and later asks for the rest of the
track with a Range request at the end of its own buffer, a player that seeks on the device asks
for the offset of the new position. The encoded stream is produced on the fly, so it has no
fixed bytes to seek in: these helpers keep, per item stream, where every encoded frame went in
the bytes the player received, and rebuild the stream from any frame by encoding it again from
a pre-roll on the same frame grid. Lossless output comes out identical to what was sent before.
"""

from __future__ import annotations

import asyncio
import os
import time
import zlib
from bisect import bisect_right
from contextlib import aclosing, suppress
from dataclasses import dataclass, field
from math import ceil, gcd
from typing import TYPE_CHECKING, Final

from music_assistant_models.enums import ContentType

if TYPE_CHECKING:
    import logging
    from collections.abc import AsyncGenerator, Callable

    from music_assistant_models.media_items import AudioFormat

# the start of every item stream is kept, so a player that reconnects from byte 0 (which a
# Sonos does before every resume) is answered without opening the source again
RANGE_HEAD_BYTES: Final[int] = 1024 * 1024
# seconds encoded ahead of the requested frame, so the DSP filters and the resampler settle
# to the state they had in the original stream before the first byte that is served
RANGE_PREROLL_SECONDS: Final[int] = 15
# a re-encode keeps running this long after its last reader left, so the follow-up requests a
# player sends around one position (a Sonos sends several per seek) need no encode of their own
RANGE_ENCODE_HOLD_SECONDS: Final[int] = 15
# frames before the requested one that a re-encode keeps, for requests a little earlier
RANGE_ENCODE_KEEP_BEFORE_SECONDS: Final[int] = 3
# how far a re-encode runs ahead of its furthest reader, and what it keeps in all
RANGE_ENCODE_AHEAD_BYTES: Final[int] = 8 * 1024 * 1024
RANGE_ENCODE_MAX_BYTES: Final[int] = 16 * 1024 * 1024
# a request this far beyond what a re-encode produced so far waits for it instead of starting
# another encode
RANGE_ENCODE_REACH_SECONDS: Final[int] = 10
# a re-encode serves the requests around the one it last served; a jump further away is a new
# seek and gets its own encode (a Sonos Amp rejected a seek answered from an encode that was
# still streaming another position to it)
RANGE_ENCODE_NEAR_SECONDS: Final[int] = 5
# how far before a segment a request is placed back from it by real frame sizes
RANGE_BACK_REACH_BYTES: Final[int] = 512 * 1024
# the announced length must not fall short of the body: a player stops at the length
RANGE_LENGTH_MARGIN: Final[float] = 1.05
RANGE_MAX_STATES: Final[int] = 8
RANGE_CODECS: Final[tuple[ContentType, ...]] = (
    ContentType.FLAC,
    ContentType.WAV,
    ContentType.MP3,
    ContentType.AAC,
)
# WAV has no frames: blocks of this many samples stand in for them
WAV_BLOCK_SAMPLES: Final[int] = 4096
# matches the -frame_size the FLAC encoder runs with (see helpers/ffmpeg.py)
FLAC_FRAME_SAMPLES: Final[int] = 4096


def byte_ranges_enabled(player_id: str) -> bool:
    """
    Return whether item streams to this player answer byte-range requests.

    :param player_id: Player the stream is for.
    """
    # prototype opt-in, to become a value of the player's HTTP profile
    return player_id in os.environ.get("MA_RANGE_PLAYERS", "").split(",")


def parse_range_start(value: str | None) -> int | None:
    """
    Return the first byte asked for by a single-range Range header.

    Only 'bytes=N-' and 'bytes=N-M' are recognised; anything else counts as no range.

    :param value: The Range header of the request.
    """
    if not value or not value.startswith("bytes="):
        return None
    spec = value.removeprefix("bytes=").strip()
    if "," in spec:
        return None
    start, sep, _ = spec.partition("-")
    start = start.strip()
    if not sep or not start.isdigit():
        return None
    return int(start)


def frame_samples_for(content_type: ContentType, sample_rate: int) -> int:
    """
    Return the number of samples per frame the encoder produces for a format.

    :param content_type: Output codec.
    :param sample_rate: Output sample rate.
    """
    if content_type == ContentType.FLAC:
        return FLAC_FRAME_SAMPLES
    if content_type == ContentType.MP3:
        return 1152 if sample_rate >= 32000 else 576
    if content_type == ContentType.AAC:
        return 1024
    return WAV_BLOCK_SAMPLES


# -- FLAC frame headers --


def _crc_table(poly: int, width: int) -> tuple[int, ...]:
    top = 1 << (width - 1)
    mask = (1 << width) - 1
    table = []
    for byte in range(256):
        crc = byte << (width - 8)
        for _ in range(8):
            crc = ((crc << 1) ^ poly) if crc & top else (crc << 1)
        table.append(crc & mask)
    return tuple(table)


_CRC8_TABLE: Final = _crc_table(0x07, 8)
_CRC16_TABLE: Final = _crc_table(0x8005, 16)

_FLAC_BLOCK_SIZES: Final[dict[int, int]] = {
    1: 192,
    2: 576,
    3: 1152,
    4: 2304,
    5: 4608,
    8: 256,
    9: 512,
    10: 1024,
    11: 2048,
    12: 4096,
    13: 8192,
    14: 16384,
    15: 32768,
}


def flac_crc8(data: bytes | bytearray | memoryview) -> int:
    """Return the CRC-8 of a FLAC frame header."""
    crc = 0
    for byte in data:
        crc = _CRC8_TABLE[crc ^ byte]
    return crc


def flac_crc16(data: bytes | bytearray | memoryview) -> int:
    """Return the CRC-16 of a FLAC frame."""
    crc = 0
    table = _CRC16_TABLE
    for byte in data:
        crc = ((crc << 8) & 0xFFFF) ^ table[(crc >> 8) ^ byte]
    return crc


@dataclass(frozen=True, slots=True)
class FlacFrameHeader:
    """A parsed FLAC frame header (fixed block size)."""

    length: int
    number: int
    number_length: int
    block_size: int


class _Incomplete(Exception):
    """More bytes are needed."""


def parse_flac_frame_header(buf: bytes | bytearray, pos: int = 0) -> FlacFrameHeader | None:
    """
    Parse the fixed-block-size FLAC frame header at a position.

    :param buf: Bytes holding the header.
    :param pos: Position of the header's sync code.
    :raises _Incomplete: The buffer ends inside the header.
    """
    end = len(buf)
    if pos + 5 > end:
        raise _Incomplete
    if buf[pos] != 0xFF or buf[pos + 1] != 0xF8:
        return None
    bs_code = buf[pos + 2] >> 4
    sr_code = buf[pos + 2] & 0x0F
    if bs_code == 0 or sr_code == 0x0F:
        return None
    if buf[pos + 3] >> 4 >= 11 or buf[pos + 3] & 0x01:
        return None
    first = buf[pos + 4]
    if first < 0x80:
        extra, number = 0, first
    elif first & 0xE0 == 0xC0:
        extra, number = 1, first & 0x1F
    elif first & 0xF0 == 0xE0:
        extra, number = 2, first & 0x0F
    elif first & 0xF8 == 0xF0:
        extra, number = 3, first & 0x07
    elif first & 0xFC == 0xF8:
        extra, number = 4, first & 0x03
    elif first & 0xFE == 0xFC:
        extra, number = 5, first & 0x01
    else:
        return None
    cursor = pos + 5
    if cursor + extra > end:
        raise _Incomplete
    for _ in range(extra):
        byte = buf[cursor]
        if byte & 0xC0 != 0x80:
            return None
        number = (number << 6) | (byte & 0x3F)
        cursor += 1
    bs_extra = 1 if bs_code == 6 else 2 if bs_code == 7 else 0
    sr_extra = 1 if sr_code == 12 else 2 if sr_code in (13, 14) else 0
    if cursor + bs_extra + sr_extra + 1 > end:
        raise _Incomplete
    if bs_extra:
        block_size = int.from_bytes(buf[cursor : cursor + bs_extra], "big") + 1
    else:
        block_size = _FLAC_BLOCK_SIZES[bs_code]
    cursor += bs_extra + sr_extra
    if flac_crc8(buf[pos:cursor]) != buf[cursor]:
        return None
    return FlacFrameHeader(cursor + 1 - pos, number, 1 + extra, block_size)


def _flac_coded_number(value: int) -> bytes:
    if value < 0x80:
        return bytes((value,))
    extra = next(
        n
        for n, limit in ((1, 1 << 11), (2, 1 << 16), (3, 1 << 21), (4, 1 << 26), (5, 1 << 31))
        if value < limit
    )
    tail = []
    for _ in range(extra):
        tail.append(0x80 | (value & 0x3F))
        value >>= 6
    lead = ((0xFF << (7 - extra)) & 0xFF) | value
    return bytes((lead, *reversed(tail)))


def renumber_flac_frame(frame: bytes, number: int) -> bytes:
    """
    Return a FLAC frame with another frame number, its CRCs recomputed.

    :param frame: One complete frame.
    :param number: The frame number to carry.
    """
    header = parse_flac_frame_header(frame)
    if header is None:
        raise ValueError("Not a FLAC frame")
    if header.number == number:
        return frame
    new_header = bytearray(frame[:4])
    new_header += _flac_coded_number(number)
    new_header += frame[4 + header.number_length : header.length - 1]
    new_header.append(flac_crc8(new_header))
    body = new_header + frame[header.length : -2]
    return bytes(body + flac_crc16(body).to_bytes(2, "big"))


def patch_flac_total_samples(head: bytearray, total_samples: int) -> None:
    """
    Write the total sample count into the STREAMINFO block at the start of a FLAC stream.

    A piped encoder leaves it at 0 (unknown), which players that seek refuse to play.

    :param head: The first bytes of the stream (at least 26).
    :param total_samples: Number of samples (per channel) the stream holds.
    """
    if head[:4] != b"fLaC" or head[4] & 0x7F != 0:
        return
    # the 36-bit count starts in the low nibble of STREAMINFO byte 13
    pos = 8 + 13
    head[pos] = (head[pos] & 0xF0) | ((total_samples >> 32) & 0x0F)
    head[pos + 1 : pos + 5] = (total_samples & 0xFFFFFFFF).to_bytes(4, "big")


# -- frame scanners --


@dataclass(slots=True)
class EncodedFrame:
    """One encoded frame of a stream."""

    offset: int
    index: int
    data: bytes


class FrameScanner:
    """Split an encoded stream, fed in order, into its header and frames."""

    def __init__(self) -> None:
        """Initialize the scanner."""
        self.header: bytes | None = None
        self.frame_samples = 0
        self._buf = bytearray()
        self._buf_offset = 0
        self._index = 0

    @property
    def pending(self) -> tuple[int, int] | None:
        """Return offset and index of the frame whose bytes are still arriving."""
        if self.header is None or not self._buf:
            return None
        return self._buf_offset, self._index

    def feed(self, data: bytes) -> list[EncodedFrame]:
        """
        Add stream bytes and return the frames they complete.

        :param data: The next bytes of the stream.
        """
        self._buf += data
        frames: list[EncodedFrame] = []
        if self.header is None:
            try:
                header_length = self._header_length(self._buf)
            except _Incomplete:
                return frames
            self.header = bytes(self._buf[:header_length])
            del self._buf[:header_length]
            self._buf_offset = header_length
        while self._buf:
            try:
                length = self._frame_length(self._buf)
            except _Incomplete:
                break
            frames.append(EncodedFrame(self._buf_offset, self._index, bytes(self._buf[:length])))
            del self._buf[:length]
            self._buf_offset += length
            self._index += 1
        return frames

    def flush(self) -> list[EncodedFrame]:
        """Return what is left as the final frame, once the stream ended."""
        if self.header is None or not self._buf:
            return []
        frame = EncodedFrame(self._buf_offset, self._index, bytes(self._buf))
        self._buf_offset += len(self._buf)
        self._buf.clear()
        self._index += 1
        return [frame]

    def _header_length(self, buf: bytearray) -> int:
        """Return the length of the stream header, raise _Incomplete to wait for more."""
        raise NotImplementedError

    def _frame_length(self, buf: bytearray) -> int:
        """Return the length of the frame at the start of buf, raise _Incomplete to wait."""
        raise NotImplementedError


class FlacFrameScanner(FrameScanner):
    """FLAC: the frame ends where the next valid header with the next number starts."""

    def __init__(self) -> None:
        """Initialize the scanner."""
        super().__init__()
        self._search_from = 0

    def _header_length(self, buf: bytearray) -> int:
        if len(buf) < 4:
            raise _Incomplete
        if buf[:4] != b"fLaC":
            raise ValueError("Not a FLAC stream")
        pos = 4
        while True:
            if pos + 4 > len(buf):
                raise _Incomplete
            last = buf[pos] & 0x80
            pos += 4 + int.from_bytes(buf[pos + 1 : pos + 4], "big")
            if last:
                if pos > len(buf):
                    raise _Incomplete
                return pos

    def _frame_length(self, buf: bytearray) -> int:
        header = parse_flac_frame_header(buf)
        if header is None:
            raise ValueError("FLAC frame expected")
        if not self.frame_samples:
            self.frame_samples = header.block_size
        pos = max(self._search_from, header.length)
        while True:
            pos = buf.find(b"\xff\xf8", pos)
            if pos < 0:
                self._search_from = max(header.length, len(buf) - 1)
                raise _Incomplete
            try:
                following = parse_flac_frame_header(buf, pos)
            except _Incomplete:
                self._search_from = pos
                raise
            if following is not None and following.number == header.number + 1:
                self._search_from = 0
                return pos
            pos += 1


_MP3_BITRATES_V1: Final = (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
_MP3_BITRATES_V2: Final = (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)
_MP3_SAMPLE_RATES: Final = (44100, 48000, 32000)


def _mp3_frame_length(buf: bytearray, pos: int) -> int:
    if pos + 4 > len(buf):
        raise _Incomplete
    if buf[pos] != 0xFF or buf[pos + 1] & 0xE0 != 0xE0:
        raise ValueError("MP3 frame expected")
    version = (buf[pos + 1] >> 3) & 0x03
    bitrate_index = buf[pos + 2] >> 4
    rate_index = (buf[pos + 2] >> 2) & 0x03
    if version == 1 or bitrate_index in (0, 15) or rate_index == 3:
        raise ValueError("Invalid MP3 frame header")
    padding = (buf[pos + 2] >> 1) & 0x01
    # MPEG 1, 2 and 2.5 halve the sample rate each
    sample_rate = _MP3_SAMPLE_RATES[rate_index] >> {3: 0, 2: 1, 0: 2}[version]
    if version == 3:
        return 144000 * _MP3_BITRATES_V1[bitrate_index] // sample_rate + padding
    return 72000 * _MP3_BITRATES_V2[bitrate_index] // sample_rate + padding


class Mp3FrameScanner(FrameScanner):
    """MP3: an optional ID3v2 tag and Xing/Info frame form the header."""

    def _header_length(self, buf: bytearray) -> int:
        pos = 0
        if len(buf) < 10:
            raise _Incomplete
        if buf[:3] == b"ID3":
            size = 0
            for byte in buf[6:10]:
                size = (size << 7) | (byte & 0x7F)
            pos = 10 + size + (10 if buf[5] & 0x10 else 0)
        length = _mp3_frame_length(buf, pos)
        if pos + length > len(buf):
            raise _Incomplete
        if b"Xing" in buf[pos : pos + 64] or b"Info" in buf[pos : pos + 64]:
            pos += length
        return pos

    def _frame_length(self, buf: bytearray) -> int:
        length = _mp3_frame_length(buf, 0)
        if length > len(buf):
            raise _Incomplete
        return length


class AdtsFrameScanner(FrameScanner):
    """AAC in ADTS: every frame carries its length."""

    def _header_length(self, buf: bytearray) -> int:
        return 0

    def _frame_length(self, buf: bytearray) -> int:
        if len(buf) < 7:
            raise _Incomplete
        if buf[0] != 0xFF or buf[1] & 0xF6 != 0xF0:
            raise ValueError("ADTS frame expected")
        length = ((buf[3] & 0x03) << 11) | (buf[4] << 3) | (buf[5] >> 5)
        if length > len(buf):
            raise _Incomplete
        return length


class WavFrameScanner(FrameScanner):
    """WAV: the RIFF header up to the data chunk, then blocks of WAV_BLOCK_SAMPLES."""

    def __init__(self) -> None:
        """Initialize the scanner."""
        super().__init__()
        self.frame_samples = WAV_BLOCK_SAMPLES
        self._block_bytes = 0

    def _header_length(self, buf: bytearray) -> int:
        if len(buf) < 12:
            raise _Incomplete
        if buf[:4] != b"RIFF" or buf[8:12] != b"WAVE":
            raise ValueError("Not a WAV stream")
        pos = 12
        while True:
            if pos + 8 > len(buf):
                raise _Incomplete
            chunk_id = bytes(buf[pos : pos + 4])
            size = int.from_bytes(buf[pos + 4 : pos + 8], "little")
            if chunk_id == b"data":
                if not self._block_bytes:
                    raise ValueError("WAV data before fmt chunk")
                return pos + 8
            if chunk_id == b"fmt ":
                if pos + 22 > len(buf):
                    raise _Incomplete
                block_align = int.from_bytes(buf[pos + 20 : pos + 22], "little")
                self._block_bytes = block_align * WAV_BLOCK_SAMPLES
            pos += 8 + size + (size & 1)

    def _frame_length(self, buf: bytearray) -> int:
        if len(buf) < self._block_bytes:
            raise _Incomplete
        return self._block_bytes


def create_frame_scanner(content_type: ContentType) -> FrameScanner:
    """
    Return a frame scanner for an output codec.

    :param content_type: One of RANGE_CODECS.
    """
    if content_type == ContentType.FLAC:
        return FlacFrameScanner()
    if content_type == ContentType.MP3:
        return Mp3FrameScanner()
    if content_type == ContentType.AAC:
        return AdtsFrameScanner()
    if content_type == ContentType.WAV:
        return WavFrameScanner()
    raise ValueError(f"No byte-range support for {content_type}")


# -- per-stream state --


@dataclass
class RangeSegment:
    """The frames one response placed in the stream, from its first byte on."""

    start: int
    first_frame: int = -1
    frame_offsets: list[int] = field(default_factory=list)
    end: int = 0
    # offset just past the last frame, once the encoder reached the end of the item
    stream_end: int | None = None

    def note_frame(self, index: int, offset: int) -> None:
        """
        Record where a frame starts.

        :param index: Frame number from the stream start.
        :param offset: Offset of its first byte in the stream.
        """
        if self.first_frame < 0:
            self.first_frame = index
        if index == self.first_frame + len(self.frame_offsets):
            self.frame_offsets.append(offset)

    def locate(self, offset: int) -> tuple[int, int] | None:
        """
        Return number and start offset of the sent frame holding a stream offset.

        :param offset: Offset in the stream.
        """
        if not self.frame_offsets or not self.frame_offsets[0] <= offset < self.end:
            return None
        pos = bisect_right(self.frame_offsets, offset) - 1
        return self.first_frame + pos, self.frame_offsets[pos]


@dataclass(frozen=True, slots=True)
class RangePlan:
    """How a response from a stream offset is produced."""

    offset: int
    frame: int
    skip: int
    preroll_frame: int
    seek_seconds: int
    trim_samples: int
    estimated: bool


@dataclass
class ByteRangeState:
    """What was sent of one item stream, in the byte numbering the player sees."""

    content_type: ContentType
    sample_rate: int
    pcm_sample_rate: int
    content_length: int
    total_samples: int
    start_seconds: int
    frame_samples: int
    head: bytearray = field(default_factory=bytearray)
    head_complete: bool = False
    segments: list[RangeSegment] = field(default_factory=list)
    frame_crcs: dict[int, int] = field(default_factory=dict)
    header_size: int | None = None
    # bytes of one WAV block (WAV_BLOCK_SAMPLES samples)
    frame_bytes: int = 0
    # WAV: the header sent in place of the encoder's, so the announced length is the header
    # plus whole samples
    stream_header: bytes | None = None
    encoders: list[RangeEncoder] = field(default_factory=list)

    @property
    def total_frames(self) -> int:
        """Return the number of frames the announced sample count spans."""
        return ceil(self.total_samples / self.frame_samples)

    @property
    def end_frame(self) -> int | None:
        """Return the number of frames the item really has, once an encode reached its end."""
        ends = [
            seg.first_frame + len(seg.frame_offsets)
            for seg in self.segments
            if seg.stream_end is not None and seg.frame_offsets
        ]
        return min(ends) if ends else None

    def ended_at(self, offset: int) -> int | None:
        """
        Return the offset of a stream end a request continues from, None if it continues none.

        A player that received a stream up to its real end asks for the rest from there.

        :param offset: First byte asked for.
        """
        for segment in self.segments:
            if segment.stream_end is not None and segment.stream_end == offset:
                return segment.stream_end
        return None

    @property
    def head_usable(self) -> bool:
        """Return whether the head can answer a request from byte 0."""
        return self.head_complete or len(self.head) >= RANGE_HEAD_BYTES

    def plan(self, offset: int) -> RangePlan | None:
        """
        Return how to produce the stream from an offset, None if it lies past the end.

        :param offset: First byte to produce; past the stream header.
        """
        estimated = False
        for segment in reversed(self.segments):
            if found := segment.locate(offset):
                frame, frame_offset = found
                skip = offset - frame_offset
                break
        else:
            if found := self._locate_before_segment(offset):
                frame, frame_offset = found
            else:
                frame, frame_offset = self._estimate_frame(offset)
                estimated = True
            skip = offset - frame_offset
        if frame >= self.total_frames or (
            (end_frame := self.end_frame) is not None and frame >= end_frame
        ):
            return None
        preroll_frames = ceil(RANGE_PREROLL_SECONDS * self.sample_rate / self.frame_samples)
        preroll_frame = max(0, frame - preroll_frames)
        # the encode starts on a whole PCM sample that falls on the frame grid
        step = self.sample_rate // gcd(self.frame_samples * self.pcm_sample_rate, self.sample_rate)
        preroll_frame -= preroll_frame % step
        pcm_start = preroll_frame * self.frame_samples * self.pcm_sample_rate // self.sample_rate
        return RangePlan(
            offset=offset,
            frame=frame,
            skip=skip,
            preroll_frame=preroll_frame,
            seek_seconds=self.start_seconds + pcm_start // self.pcm_sample_rate,
            trim_samples=pcm_start % self.pcm_sample_rate,
            estimated=estimated,
        )

    def close(self) -> None:
        """Stop the re-encodes still running for this stream."""
        for encoder in self.encoders:
            encoder.cancel()
        self.encoders.clear()

    def frames_for(self, seconds: float) -> int:
        """
        Return the number of frames that span a duration.

        :param seconds: Duration in seconds.
        """
        return ceil(seconds * self.sample_rate / self.frame_samples)

    def record_head(self, offset: int, data: bytes) -> None:
        """
        Keep stream bytes that fall within the head.

        :param offset: Offset of data in the stream.
        :param data: Bytes sent at that offset.
        """
        if offset == len(self.head) and offset < RANGE_HEAD_BYTES:
            self.head += data[: RANGE_HEAD_BYTES - offset]

    def _locate_before_segment(self, offset: int) -> tuple[int, int] | None:
        # a player that just received a segment may ask again a little before it: the frames
        # before it are then placed back from its first frame by their real sizes, so what it
        # holds and what it gets now join up
        for segment in reversed(self.segments):
            if not segment.frame_offsets:
                continue
            number, position = segment.first_frame, segment.frame_offsets[0]
            # only what the player received counts
            if segment.end <= position or not offset < position <= offset + RANGE_BACK_REACH_BYTES:
                continue
            while position > offset:
                number -= 1
                if (data := self._frame_data(number)) is None:
                    break
                position -= len(data)
            else:
                return number, position
        return None

    def _frame_data(self, number: int) -> bytes | None:
        for encoder in reversed(self.encoders):
            if (data := encoder.frames.get(number)) is not None:
                return data
        return None

    def _estimate_frame(self, offset: int) -> tuple[int, int]:
        if self.content_type == ContentType.WAV and self.header_size is not None:
            block_bytes = self.frame_bytes
            frame = (offset - self.header_size) // block_bytes
            return frame, self.header_size + frame * block_bytes
        # past everything sent: a player seeking there takes the position as the same share of
        # the announced samples as the offset is of the announced length (a Sonos does), and
        # checks it against the frame it gets back, so the frame is chosen the same way
        return offset * self.total_frames // max(self.content_length, 1), offset


@dataclass
class RangeStats:
    """What a range response served, for the verification log."""

    first_frame: int | None = None
    frames_checked: int = 0
    frames_mismatched: int = 0
    first_mismatch: int | None = None
    preroll_seconds: float | None = None
    plan: RangePlan | None = None
    segment: RangeSegment | None = None
    reused: bool = False
    player_name: str = ""


def _note_frames(
    state: ByteRangeState, segment: RangeSegment, scanner: FrameScanner, frames: list[EncodedFrame]
) -> None:
    for frame in frames:
        segment.note_frame(frame.index, frame.offset)
        state.frame_crcs[frame.index] = zlib.crc32(frame.data)
    if pending := scanner.pending:
        segment.note_frame(pending[1], pending[0])


async def record_stream(
    state: ByteRangeState,
    segment: RangeSegment,
    encoded: AsyncGenerator[bytes],
) -> AsyncGenerator[bytes]:
    """
    Pass an item stream served from byte 0 through, recording its frames and head.

    :param state: State of the item stream.
    :param segment: Segment of this response (starting at 0).
    :param encoded: The encoded stream.
    """
    scanner = create_frame_scanner(state.content_type)
    patch_pending = state.content_type == ContentType.FLAC
    replace_header = state.stream_header is not None
    held = bytearray()
    offset = 0
    async with aclosing(encoded):
        async for encoded_chunk in encoded:
            chunk = encoded_chunk
            if replace_header:
                held += chunk
                try:
                    header_length = WavFrameScanner()._header_length(held)
                except _Incomplete:
                    continue
                assert state.stream_header is not None
                chunk = state.stream_header + bytes(held[header_length:])
                replace_header = False
            if patch_pending:
                held += chunk
                if len(held) < 26:
                    continue
                patch_flac_total_samples(held, state.total_samples)
                chunk = bytes(held)
                patch_pending = False
            frames = scanner.feed(chunk)
            if state.header_size is None and scanner.header is not None:
                state.header_size = len(scanner.header)
            _note_frames(state, segment, scanner, frames)
            state.record_head(offset, chunk)
            offset += len(chunk)
            yield chunk
    _note_frames(state, segment, scanner, scanner.flush())
    if segment.frame_offsets:
        segment.stream_end = offset
    if offset <= RANGE_HEAD_BYTES:
        state.head_complete = True


class RangeEncoder:
    """A re-encode of an item stream from a pre-roll, serving every request that falls in it."""

    def __init__(
        self,
        state: ByteRangeState,
        plan: RangePlan,
        encode_from: Callable[[RangePlan, Callable[[], bool]], AsyncGenerator[bytes]],
    ) -> None:
        """
        Start the encode.

        :param state: State of the item stream.
        :param plan: The plan of the request that started it.
        :param encode_from: Returns the stream encoded from a plan's pre-roll frame.
        """
        self.state = state
        self.plan = plan
        self.first_kept = max(
            plan.preroll_frame, plan.frame - state.frames_for(RANGE_ENCODE_KEEP_BEFORE_SECONDS)
        )
        self.frames: dict[int, bytes] = {}
        self.next_frame = self.first_kept
        self.done = False
        self.reached_end = False
        self.error: Exception | None = None
        self._encode_from = encode_from
        self._changed = asyncio.Condition()
        self._readers = 0
        self._read_position = plan.frame
        self._last_request = plan.frame
        self._last_read = time.monotonic()
        self._size = 0
        self._task = asyncio.get_running_loop().create_task(self._run())

    @property
    def idle(self) -> bool:
        """Return whether no reader used this encode for the hold time."""
        return self._readers == 0 and time.monotonic() - self._last_read > RANGE_ENCODE_HOLD_SECONDS

    def covers(self, frame: int) -> bool:
        """
        Return whether this encode holds a frame, or will produce it shortly.

        :param frame: Frame number.
        """
        if self.error is not None or frame < self.first_kept or self.idle:
            return False
        if abs(frame - self._last_request) > self.state.frames_for(RANGE_ENCODE_NEAR_SECONDS):
            return False
        if frame in self.frames:
            return True
        if frame < self.next_frame or self.done:
            return False
        return frame <= self.next_frame + self.state.frames_for(RANGE_ENCODE_REACH_SECONDS)

    def cancel(self) -> None:
        """Stop the encode."""
        self._task.cancel()

    async def read(
        self, plan: RangePlan, segment: RangeSegment, stats: RangeStats
    ) -> AsyncGenerator[bytes]:
        """
        Yield the stream from a planned offset, out of the frames of this encode.

        :param plan: Where the response starts.
        :param segment: Segment of the response (starting at the planned offset).
        :param stats: Receives what was served and how it compared with earlier sends.
        """
        state = self.state
        number = plan.frame
        self._last_request = number
        skip = plan.skip
        offset = plan.offset - plan.skip
        started = time.monotonic()
        self._readers += 1
        try:
            while True:
                self._read_position = max(self._read_position, number)
                self._last_read = time.monotonic()
                out = bytearray()
                while (data := self.frames.get(number)) is not None and len(out) < 256 * 1024:
                    crc = zlib.crc32(data)
                    if (sent_crc := state.frame_crcs.get(number)) is not None:
                        stats.frames_checked += 1
                        if sent_crc != crc:
                            stats.frames_mismatched += 1
                            if stats.first_mismatch is None:
                                stats.first_mismatch = number
                    else:
                        state.frame_crcs[number] = crc
                    if stats.first_frame is None:
                        stats.first_frame = number
                        stats.preroll_seconds = time.monotonic() - started
                    segment.note_frame(number, offset)
                    out += data[skip:]
                    skip = 0
                    offset += len(data)
                    number += 1
                if out:
                    await self._notify()
                    yield bytes(out)
                    continue
                if self.error is not None:
                    raise self.error
                if self.done or number < self.next_frame:
                    break
                async with self._changed:
                    await self._changed.wait()
            if self.reached_end and stats.first_frame is not None and number >= self.next_frame:
                segment.stream_end = offset
        finally:
            self._readers -= 1
            self._last_read = time.monotonic()

    async def _notify(self) -> None:
        async with self._changed:
            self._changed.notify_all()

    def _consumer_connected(self) -> bool:
        return not self.idle

    async def _run(self) -> None:
        state = self.state
        scanner = create_frame_scanner(state.content_type)
        stopped = False
        try:
            async with aclosing(self._encode_from(self.plan, self._consumer_connected)) as encoded:
                async for chunk in encoded:
                    for frame in scanner.feed(chunk):
                        self._add(frame)
                    await self._notify()
                    if await self._should_stop():
                        stopped = True
                        break
            if not stopped:
                for frame in scanner.flush():
                    self._add(frame)
                self.reached_end = True
        except asyncio.CancelledError:
            raise
        except Exception as err:
            self.error = err
        finally:
            self.done = True
            await asyncio.shield(self._notify())

    def _add(self, frame: EncodedFrame) -> None:
        number = self.plan.preroll_frame + frame.index
        if number < self.first_kept:
            return
        data = frame.data
        if self.state.content_type == ContentType.FLAC:
            data = renumber_flac_frame(data, number)
        self.frames[number] = data
        self._size += len(data)
        self.next_frame = number + 1
        # drop the oldest frames once over the cap, keeping those just before the readers
        floor = self._read_position - self.state.frames_for(RANGE_ENCODE_KEEP_BEFORE_SECONDS)
        while self._size > RANGE_ENCODE_MAX_BYTES and self.frames:
            oldest = next(iter(self.frames))
            if oldest >= floor:
                break
            self._size -= len(self.frames.pop(oldest))

    async def _should_stop(self) -> bool:
        # paces the encode to its readers: it runs ahead of the furthest one only so far
        while True:
            if self.idle:
                return True
            ahead = sum(
                len(data) for number, data in self.frames.items() if number >= self._read_position
            )
            if ahead < RANGE_ENCODE_AHEAD_BYTES:
                return False
            async with self._changed:
                with suppress(TimeoutError):
                    await asyncio.wait_for(self._changed.wait(), 1)


async def serve_from(
    state: ByteRangeState,
    start: int,
    encode_from: Callable[[RangePlan, Callable[[], bool]], AsyncGenerator[bytes]],
    stats: RangeStats,
    logger: logging.Logger,
) -> AsyncGenerator[bytes]:
    """
    Produce the item stream from an offset: the head first, then a re-encode.

    :param state: State of the item stream.
    :param start: First byte to produce.
    :param encode_from: Returns the stream encoded from a plan's pre-roll frame; its second
        argument reports whether anyone still waits for the audio.
    :param stats: Receives what was served.
    :param logger: Logger for the served path.
    """
    if start < len(state.head) and state.head_usable:
        stats_path = "head"
        logger.debug("byte range from %s: head (%s bytes)", start, len(state.head) - start)
        yield bytes(state.head[start:])
        if state.head_complete:
            return
        start = len(state.head)
    else:
        stats_path = "re-encode"
    if (plan := state.plan(start)) is None:
        return
    stats.plan = plan
    state.encoders = [enc for enc in state.encoders if not (enc.done and enc.idle)]
    encoder = next((enc for enc in reversed(state.encoders) if enc.covers(plan.frame)), None)
    reused = encoder is not None
    if encoder is None:
        encoder = RangeEncoder(state, plan, encode_from)
        state.encoders.append(encoder)
    stats.reused = reused
    logger.debug(
        "byte range from %s (%s) on %s: frame %s +%s, %s, %s",
        start,
        stats_path,
        stats.player_name,
        plan.frame,
        plan.skip,
        "estimated" if plan.estimated else "mapped",
        f"frames of the encode from frame {encoder.plan.preroll_frame}"
        if reused
        else f"pre-roll from frame {plan.preroll_frame} ({plan.seek_seconds}s"
        f" + {plan.trim_samples} samples)",
    )
    segment = RangeSegment(start=start, end=start)
    state.segments.append(segment)
    stats.segment = segment
    async for chunk in encoder.read(plan, segment, stats):
        yield chunk


async def trim_pcm(stream: AsyncGenerator[bytes], trim_bytes: int) -> AsyncGenerator[bytes]:
    """
    Drop the first bytes of a PCM stream.

    :param stream: The PCM stream.
    :param trim_bytes: Number of bytes to drop.
    """
    async with aclosing(stream):
        async for chunk in stream:
            if trim_bytes:
                if len(chunk) <= trim_bytes:
                    trim_bytes -= len(chunk)
                    continue
                yield chunk[trim_bytes:]
                trim_bytes = 0
                continue
            yield chunk


def announced_length(audio_format: AudioFormat, seconds: int) -> int:
    """
    Return the content length to announce for an item stream: never less than the body.

    :param audio_format: Output format.
    :param seconds: Duration of the stream, rounded up.
    """
    pcm_size = (
        audio_format.sample_rate * seconds * audio_format.channels * audio_format.bit_depth // 8
    )
    if audio_format.content_type == ContentType.WAV:
        # a WAV body must hold whole samples: the 44 byte header plus the PCM, exactly
        return 44 + pcm_size
    if audio_format.content_type == ContentType.FLAC:
        # FLAC never compresses to more than the PCM it holds (plus frame headers)
        size = int(pcm_size * 1.01)
    elif audio_format.content_type == ContentType.MP3:
        size = int(320000 / 8 * seconds * RANGE_LENGTH_MARGIN)
    else:
        size = int(256000 / 8 * seconds * RANGE_LENGTH_MARGIN)
    # room for the stream header
    return size + 64 * 1024
