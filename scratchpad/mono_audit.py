# ruff: noqa
"""
Classify every provider's icon_monochrome file.

The frontend shows icon_monochrome as-is on the dark theme and CSS-inverts it on the light
theme, so the file must be pure white on transparent, a vector, and <= 5 KB.
Run from server/: .venv/bin/python scratchpad/mono_audit.py
"""

import base64
import io
import re
import warnings
from pathlib import Path
from urllib.parse import unquote

warnings.simplefilter("ignore", DeprecationWarning)

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True  # some embedded PNGs are cut short; measure what is there

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / "music_assistant" / "providers"
LIMIT_SVG = 5 * 1024
LIMIT_PNG = 20 * 1024
WHITE = {"#fff", "#ffffff", "white", "rgb(100%,100%,100%)", "rgb(255,255,255)"}

# status -> short meaning; "ok" needs no work
STATUS = {
    "ok": "white vector within budget",
    "missing": "no monochrome file",
    "black": "vector drawn in black / non-white colour: invisible on both themes",
    "bw": "black + white two-tone: works under inversion (tile and glyph swap), but not a true monochrome",
    "colour": "vector with brand colours: inverts to wrong colours on the light theme",
    "png-dark": "raster, dark: invisible on both themes",
    "png-white": "raster, white: renders, but oversized and grandfathered",
    "png-mixed": "raster, mixed luminance: check by eye",
    "oversize": "white vector but over 5 KB",
}


def _strip(text: str) -> str:
    return re.sub(
        r"<sodipodi:namedview.*?/>|<metadata>.*?</metadata>|<!--.*?-->", "", text, flags=re.DOTALL
    )


def _colours(text: str) -> set[str]:
    found = set(re.findall(r"(?:fill|stroke|stop-color)\s*[:=]\s*\"?\s*([#\w(),%]+)", text))
    return {c.lower() for c in found} - {"none", "evenodd", "nonzero"}


def _hex_luminance(value: str) -> float | None:
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", value)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def is_white(colour: str) -> bool:
    if colour in WHITE:
        return True
    lum = _hex_luminance(colour)
    return lum is not None and lum >= 0.9


def is_black(colour: str) -> bool:
    if colour in {"black", "#000", "#000000", "rgb(0,0,0)", "rgb(0%,0%,0%)"}:
        return True
    lum = _hex_luminance(colour)
    return lum is not None and lum <= 0.12


def _png_luminance(data: bytes) -> float:
    """Alpha-weighted mean luminance 0..1 of the opaque pixels."""
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    px = img.getdata()
    total = 0.0
    weight = 0.0
    for r, g, b, a in px:
        if a == 0:
            continue
        total += (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 * a
        weight += a
    return total / weight if weight else 0.0


def classify(domain: str) -> tuple[str, str]:
    """Return (status, detail) for a provider's monochrome icon."""
    d = PROVIDERS / domain
    svg = d / "icon_monochrome.svg"
    png = d / "icon_monochrome.png"
    if svg.exists():
        raw = svg.read_bytes()
        text = _strip(raw.decode(errors="replace"))
        size = len(raw)
        # base64 may be wrapped with literal newlines or XML-escaped ones (&#10;)
        m = re.search(r"data:image/png;base64,((?:[A-Za-z0-9+/=%\s]|&#1[03];)+)", text)
        if m:
            b64 = re.sub(r"\s|&#1[03];", "", unquote(m.group(1)))
            try:
                lum = _png_luminance(base64.b64decode(b64))
            except Exception as err:
                return "png-mixed", f"svg-wrapped PNG, unreadable ({err}), {size} B"
            kind = "png-white" if lum >= 0.85 else "png-dark" if lum < 0.5 else "png-mixed"
            return kind, f"svg-wrapped PNG, luminance {lum:.2f}, {size} B"
        cols = _colours(text)
        # elements with no fill at all default to black
        has_unfilled = bool(
            re.search(r"<(path|rect|circle|ellipse|polygon)\b(?![^>]*fill)[^>]*>", text)
        ) and not re.search(r"<(svg|g)\b[^>]*fill", text)
        if has_unfilled and not cols:
            return "black", f"no fill set (defaults to black), {size} B"
        others = {c for c in cols if not is_white(c)}
        if others:
            if len(others) == 1 and not (cols - others):
                return "black", f"single colour {sorted(others)[0]}, {size} B"
            if all(is_black(c) for c in others):
                return "bw", f"{', '.join(sorted(cols))}, {size} B"
            return "colour", f"{', '.join(sorted(cols))}, {size} B"
        if size > LIMIT_SVG:
            return "oversize", f"white, {size} B"
        return "ok", f"white, {size} B"
    if png.exists():
        raw = png.read_bytes()
        lum = _png_luminance(raw)
        kind = "png-white" if lum >= 0.85 else "png-dark" if lum < 0.5 else "png-mixed"
        return kind, f"icon_monochrome.png, luminance {lum:.2f}, {len(raw)} B"
    return "missing", ""


def has_icon(domain: str) -> bool:
    d = PROVIDERS / domain
    return (d / "icon.svg").exists() or (d / "icon.png").exists()


def audit() -> dict[str, tuple[str, str]]:
    return {
        d.name: classify(d.name)
        for d in sorted(PROVIDERS.iterdir())
        if d.is_dir() and not d.name.startswith("__") and has_icon(d.name)
    }


if __name__ == "__main__":
    result = audit()
    by_status: dict[str, list[str]] = {}
    for domain, (status, detail) in result.items():
        by_status.setdefault(status, []).append(f"{domain} ({detail})" if detail else domain)
    for status in STATUS:
        items = by_status.get(status, [])
        print(f"\n== {status} [{len(items)}] — {STATUS[status]}")
        for item in items:
            print("  ", item)
