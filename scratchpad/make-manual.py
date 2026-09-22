# ruff: noqa
"""
User-directed, per-provider icon edits (2026-09-22 review). Idempotent: every step derives
its output from a file that this script does not modify, or from the branch-base version.

Run from server/: .venv/bin/python scratchpad/make-manual.py
"""

import base64
import io
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageOps

from iconlib import BASE, PROVIDERS, ROOT, add_note
from trace import fit_budget, png_from_svg

PLAN = Path(__file__).parent / "mono-plan.json"
done: list[str] = []


def original(domain: str, name: str) -> bytes:
    """The file as it was at the branch base."""
    return subprocess.check_output(
        ["git", "show", f"{BASE}:music_assistant/providers/{domain}/{name}"], cwd=ROOT
    )


def swap(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        assert old in text, f"{old!r} not found"
        text = text.replace(old, new)
    return text


def write(domain: str, name: str, data: bytes | str, note: str) -> None:
    """Write the file the way the repo's pre-commit hooks want it: no trailing whitespace, one final newline."""
    path = PROVIDERS / domain / name
    text = data.decode() if isinstance(data, bytes) else data
    text = "\n".join(line.rstrip() for line in text.splitlines()).rstrip("\n") + "\n"
    path.write_text(text)
    done.append(f"{domain}/{name}: {note} ({path.stat().st_size} B)")


def _hex(r: float, g: float, b: float) -> str:
    return "#%02x%02x%02x" % (round(r), round(g), round(b))


def _parse_colour(value: str) -> tuple[float, float, float] | None:
    value = value.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", value)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    m = re.fullmatch(r"rgb\(\s*([\d.]+)%\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)", value)
    if m:
        return tuple(float(x) * 2.55 for x in m.groups())  # type: ignore[return-value]
    m = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", value)
    if m:
        return tuple(float(x) for x in m.groups())  # type: ignore[return-value]
    return None


def greyscale(svg: str, lift: float = 0.45) -> str:
    """
    Map every fill/stroke/stop colour to a grey by luminance, brightened so it reads on a dark
    surface (grey = lift + (1 - lift) * luminance). White and black stay as they are.
    """

    def to_grey(m: re.Match) -> str:
        rgb = _parse_colour(m.group(3))
        if rgb is None:
            return m.group(0)
        lum = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
        if lum >= 0.98 or lum <= 0.02:
            return m.group(0)
        g = 255 * (lift + (1 - lift) * lum)
        return f"{m.group(1)}{m.group(2)}{_hex(g, g, g)}"

    return re.sub(
        r"(fill|stroke|stop-color)(\s*[:=]\s*\"?\s*)(#[0-9a-fA-F]{3,6}|rgb\([^)]*\))", to_grey, svg
    )


def recolour(
    img: Image.Image,
    light: tuple[int, int, int] | None = None,
    dark: tuple[int, int, int] | None = None,
    all_: bool = False,
    threshold: int = 128,
) -> Image.Image:
    """Recolour opaque pixels: light ones (luminance >= threshold) to `light`, dark ones to `dark`; all_=True recolours every opaque pixel to `light`."""
    out = img.copy()
    px = out.load()
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if all_ or (lum >= threshold and light is not None):
                px[x, y] = (*light, a)
            elif lum < threshold and dark is not None:
                px[x, y] = (*dark, a)
    return out


def png_svg(img: Image.Image, width: int) -> str:
    """Wrap a PIL image as an svg with one embedded palette PNG at the given width."""
    small = img.resize((width, round(img.size[1] * width / img.size[0])), Image.LANCZOS).quantize(
        64
    )
    buf = io.BytesIO()
    small.save(buf, "PNG", optimize=True)
    w, h = small.size
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}">'
        f'<image width="{w}" height="{h}" xlink:href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/></svg>'
    )


def reencode_png_in_svg(
    svg: str,
    width: int,
    invert: bool = False,
    grey: bool = False,
    black_to: tuple[int, int, int] | None = None,
) -> str:
    """Re-encode the embedded PNG at the given width as a 64-colour palette PNG, after optional pixel edits."""
    m = re.search(r"data:image/png;base64,((?:[A-Za-z0-9+/=%\s]|&#1[03];)+)", svg)
    raw = base64.b64decode(re.sub(r"\s|&#1[03];", "", m.group(1)))
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    if invert:
        rgb = ImageOps.invert(img.convert("RGB"))
        img = Image.merge("RGBA", (*rgb.split(), img.getchannel("A")))
    if grey:
        # lifted greyscale, like greyscale() for vectors: grey = 0.45 + 0.55 * luminance
        lum = img.convert("L").point(lambda v: round(255 * (0.45 + 0.55 * v / 255)))
        img = Image.merge("RGBA", (lum, lum, lum, img.getchannel("A")))
    if black_to is not None:
        img = recolour(img, dark=black_to, threshold=40)
    img = img.resize((width, round(img.size[1] * width / img.size[0])), Image.LANCZOS).quantize(64)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    svg = svg[: m.start(1)] + base64.b64encode(buf.getvalue()).decode() + svg[m.end(1) :]
    svg = re.sub(r"<defs>.*?</defs>\s*", "", svg, flags=re.DOTALL)
    svg = re.sub(r'<g filter="[^"]*">\s*(<image.*?/>)\s*</g>', r"\1", svg, flags=re.DOTALL)
    return svg


def minify_svg(svg: str, decimals: int, tight: bool = False) -> str:
    """Drop editor metadata and redundant attributes, round path coordinates, collapse whitespace."""
    if tight:
        # gradient-heavy file: style attributes to plain attributes, defaults dropped, ids shortened,
        # percentage rgb() to hex, transform matrices to integers
        svg = re.sub(
            r'style="([^"]*)"',
            lambda m: " ".join(
                f'{k.strip()}="{v.strip()}"'
                for k, v in (p.split(":", 1) for p in m.group(1).split(";") if ":" in p)
            ),
            svg,
        )
        svg = re.sub(
            r'\s+(stroke="none"|fill-rule="nonzero"|stop-opacity="1"|fx="0"|fy="0")', "", svg
        )
        svg = re.sub(r'\s+id="([a-z]+)(\d+)"', lambda m: f' id="{m.group(1)[0]}{m.group(2)}"', svg)
        svg = re.sub(r"url\(#([a-z]+)(\d+)\)", lambda m: f"url(#{m.group(1)[0]}{m.group(2)})", svg)
        svg = re.sub(r"rgb\([^)]*\)", lambda m: _hex(*_parse_colour(m.group(0))), svg)
        svg = re.sub(
            r'gradientTransform="[^"]*"',
            lambda m: re.sub(r"-?\d+\.\d+", lambda n: str(round(float(n.group(0)))), m.group(0)),
            svg,
        )
        svg = re.sub(
            r"-?\d+\.\d{3,}", lambda n: f"{float(n.group(0)):.2f}".rstrip("0").rstrip("."), svg
        )
    svg = re.sub(
        r"<\?xml.*?\?>|<!DOCTYPE[^>]*>|<!--.*?-->|<metadata>.*?</metadata>|<title>.*?</title>|<desc>.*?</desc>",
        "",
        svg,
        flags=re.DOTALL,
    )
    svg = re.sub(r"<sodipodi:namedview.*?/>", "", svg, flags=re.DOTALL)
    # ids are dropped only when nothing references them (gradient/clip ids must survive)
    drop_ids = "id|" if "url(#" not in svg and "href=" not in svg else ""
    svg = re.sub(
        rf'\s+({drop_ids}version|xml:space|enable-background|xmlns:xlink|xmlns:svg|xmlns:sodipodi|xmlns:inkscape|inkscape:[\w-]+|sodipodi:[\w-]+)="[^"]*"',
        "",
        svg,
    )
    # x/y/width/height are redundant on the root only (the viewBox sets the geometry)
    svg = re.sub(
        r"<svg\b[^>]*>",
        lambda m: re.sub(r'\s+(x|y|width|height)="[^"]*"', "", m.group(0)),
        svg,
        count=1,
    )

    def rnd(m: re.Match) -> str:
        r = f"{float(m.group(0)):.{decimals}f}".rstrip("0").rstrip(".")
        return "0" if r in ("", "-0") else r

    def fix_d(m: re.Match) -> str:
        d = re.sub(r"-?\d+\.\d+", rnd, m.group(2))
        d = re.sub(r"\s+", " ", d).replace(", ", ",").replace(" ,", ",")
        return f'{m.group(1)}="{d}"'

    svg = re.sub(r'\b(d|points)="([^"]*)"', fix_d, svg)
    return re.sub(r">\s+<", "><", svg).strip()


def lighten_dark_fills(svg: str, floor: float = 0.75) -> str:
    """Raise any fill darker than `floor` luminance to a light grey (for dark variants of dark marks)."""

    def fix(m: re.Match) -> str:
        rgb = _parse_colour(m.group(1))
        lum = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
        if lum >= floor:
            return m.group(0)
        g = 255 * (floor + (1 - floor) * lum)
        return f'fill="{_hex(g, g, g)}"'

    return re.sub(r'fill="(#[0-9a-fA-F]{6})"', fix, svg)


def invert_png_in_svg(svg: str) -> str:
    """Pixel-invert the embedded PNG (RGB only, alpha kept), drop any filter wrapper."""
    m = re.search(r"data:image/png;base64,((?:[A-Za-z0-9+/=%\s]|&#1[03];)+)", svg)
    raw = base64.b64decode(re.sub(r"\s|&#1[03];", "", m.group(1)))
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    rgb = ImageOps.invert(img.convert("RGB"))
    out = Image.merge("RGBA", (*rgb.split(), img.getchannel("A")))
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    svg = svg[: m.start(1)] + b64 + svg[m.end(1) :]
    svg = re.sub(r"<defs>.*?</defs>\s*", "", svg, flags=re.DOTALL)
    svg = re.sub(r'<g filter="[^"]*">\s*(<image.*?/>)\s*</g>', r"\1", svg, flags=re.DOTALL)
    return svg


# 1. demo providers: monochrome is the dark file (white tile, black bars)
for demo in ("_demo_music_provider", "_demo_player_provider", "_demo_plugin_provider"):
    write(
        demo,
        "icon_monochrome.svg",
        (PROVIDERS / demo / "icon_dark.svg").read_text(),
        "copy of icon_dark.svg",
    )

# 2. abc_radio_network: today's white icon.svg becomes the dark variant; icon.svg is inverted
abc = original("abc_radio_network", "icon.svg").decode()
write("abc_radio_network", "icon_dark.svg", abc, "the original white icon.svg")
write(
    "abc_radio_network",
    "icon.svg",
    swap(abc, [('flood-color="#000"', 'flood-color="#fff"'), ('fill="#fff"', 'fill="#000"')]),
    "original inverted: fill black, shadow white",
)

# 3. airplay: icon.svg serves dark too (no icon_dark file); its blue becomes Apple's system
#    blue for dark mode, sampled from the HIG "custom color icon set" image (#0a84ff)
write(
    "airplay",
    "icon.svg",
    swap(original("airplay", "icon.svg").decode(), [("fill:#0000ff", "fill:#0a84ff")]),
    "original with #0000ff -> #0a84ff",
)

# 4. alexa: monochrome from icon.svg, everything white (editor ids and the XML declaration
#    dropped to stay under the 5 KB budget)
alexa = swap(
    (PROVIDERS / "alexa" / "icon.svg").read_text(),
    [("fill:#05a0d1", "fill:#fff"), ("stroke:#05a0d1", "stroke:#fff")],
)
alexa = re.sub(r'\s+id="[^"]*"', "", alexa)
alexa = re.sub(r"<\?xml[^>]*\?>\s*", "", alexa)
alexa = re.sub(r"\n\s*", " ", alexa).replace("> <", "><")
write("alexa", "icon_monochrome.svg", alexa, "icon.svg with fill and stroke white")

# 5. ariacast_receiver: monochrome is icon.svg with the blues made black (white tile kept)
aria = (PROVIDERS / "ariacast_receiver" / "icon.svg").read_text()
aria = re.sub(r"fill: #(50649a|4c6298|50659b|4a6097);", "fill: #000;", aria)
assert "#50649a" not in aria
write("ariacast_receiver", "icon_monochrome.svg", aria, "icon.svg with the blues set to black")

# 6. internet_archive: dark variant from the Commons "logo and wordmark" SVG
#    (https://commons.wikimedia.org/wiki/File:Internet_Archive_logo_and_wordmark.svg, PD-shape),
#    minified to fit the 5 KB budget and filled white
ia = minify_svg(
    (Path(__file__).parent / "sources" / "Internet_Archive_logo_and_wordmark.svg").read_text(),
    decimals=1,
)
ia = ia.replace("<svg", '<svg fill="#fff"', 1)
write("internet_archive", "icon_dark.svg", ia, "Commons logo+wordmark SVG, minified, white")

# 7. lastfm_recommendations: same monochrome as lastfm_scrobble
write(
    "lastfm_recommendations",
    "icon_monochrome.svg",
    (PROVIDERS / "lastfm_scrobble" / "icon_monochrome.svg").read_text(),
    "copy of lastfm_scrobble/icon_monochrome.svg",
)

# 8. msx_bridge: the original white raster traced to a vector; that is the dark variant, and
#    icon.svg is the same vector in black so it reads on light
msx_img = png_from_svg(original("msx_bridge", "icon.svg").decode())
msx_vec = fit_budget(msx_img, colours=1)
write("msx_bridge", "icon_dark.svg", msx_vec, "original white raster traced to vector")
write(
    "msx_bridge",
    "icon.svg",
    re.sub(r'fill="#[0-9a-f]{6}"', 'fill="#000"', msx_vec),
    "same vector in black",
)

# 9. smart_playlist: monochrome from icon.svg, blue -> white, white -> black
write(
    "smart_playlist",
    "icon_monochrome.svg",
    swap(
        (PROVIDERS / "smart_playlist" / "icon.svg").read_text(),
        [('fill="#ffffff"', 'fill="#000"'), ('fill="#18bcf2"', 'fill="#fff"')],
    ),
    "icon.svg with blue -> white, white -> black",
)

# 10. theaudiodb: dark variant is icon.svg with the grey body made very light (white glyph kept)
write(
    "theaudiodb",
    "icon_dark.svg",
    swap(
        (PROVIDERS / "theaudiodb" / "icon.svg").read_text(), [('fill="#454545"', 'fill="#d9d9d9"')]
    ),
    "icon.svg with #454545 -> #d9d9d9",
)

# 11. bbc_sounds: icon.svg reads on dark, so it is the dark variant; monochrome is a lifted
#     greyscale of it (each orange mapped to a grey by luminance, brightened to read on dark)
bbc = (PROVIDERS / "bbc_sounds" / "icon.svg").read_text()
write("bbc_sounds", "icon_dark.svg", bbc, "copy of icon.svg")
write("bbc_sounds", "icon_monochrome.svg", greyscale(bbc), "icon.svg in lifted greyscale")

# 12. filesystem_onedrive: icon.svg replaced by the Commons 2025 OneDrive icon (minified to fit
#     the budget, gradient ids kept); it serves dark as-is; monochrome is its lifted greyscale
od = minify_svg(
    (
        Path(__file__).parent / "sources" / "Microsoft_OneDrive_Icon_(2025_-_present).svg"
    ).read_text(),
    decimals=0,
    tight=True,
)
write("filesystem_onedrive", "icon.svg", od, "Commons 2025 OneDrive icon, minified")
write(
    "filesystem_onedrive",
    "icon_monochrome.svg",
    greyscale(od),
    "the new icon.svg in lifted greyscale",
)

# 13. fully_kiosk: monochrome doubles as the dark variant
write(
    "fully_kiosk",
    "icon_dark.svg",
    (PROVIDERS / "fully_kiosk" / "icon_monochrome.svg").read_text(),
    "copy of icon_monochrome.svg",
)

# 14. lrclib: the icon.svg raster inverted and traced to a vector; that is the monochrome, and
#     the same file is the dark variant
lrc_img = png_from_svg(original("lrclib", "icon.svg").decode())
lrc_img = Image.merge(
    "RGBA", (*ImageOps.invert(lrc_img.convert("RGB")).split(), lrc_img.getchannel("A"))
)
lrc = fit_budget(lrc_img, colours=2)
write("lrclib", "icon_monochrome.svg", lrc, "icon.svg raster inverted and traced to vector")
write("lrclib", "icon_dark.svg", lrc, "same file as icon_monochrome.svg")

# 15. musiccast: monochrome doubles as the dark variant; its 29 KB white raster traced to a vector
write(
    "musiccast",
    "icon_dark.svg",
    fit_budget(
        png_from_svg((PROVIDERS / "musiccast" / "icon_monochrome.svg").read_text()), colours=1
    ),
    "icon_monochrome.svg raster traced to vector",
)

# 16. musicme: monochrome doubles as the dark variant, traced to a vector (monochrome kept as-is)
write(
    "musicme",
    "icon_dark.svg",
    fit_budget(
        png_from_svg((PROVIDERS / "musicme" / "icon_monochrome.svg").read_text()), colours=2
    ),
    "icon_monochrome.svg raster traced to vector",
)

# 17. nts: black tile + white text already behaves as a monochrome under the UI's inversion
write(
    "nts", "icon_monochrome.svg", (PROVIDERS / "nts" / "icon.svg").read_text(), "copy of icon.svg"
)

# 18. openai_compatible: monochrome from icon.svg, purple tile -> white, stars -> black
write(
    "openai_compatible",
    "icon_monochrome.svg",
    swap(
        (PROVIDERS / "openai_compatible" / "icon.svg").read_text(),
        [('fill="#ffffff"', 'fill="#000"'), ('fill="#7c5cff"', 'fill="#fff"')],
    ),
    "icon.svg with purple -> white, white -> black",
)

# 19. airplay: monochrome from the (original) icon.svg in white — the old one was a different logo
write(
    "airplay",
    "icon_monochrome.svg",
    swap(original("airplay", "icon.svg").decode(), [("fill:#0000ff", "fill:#fff")]),
    "original icon.svg in white",
)

# 20. amplipi: the wordmark PNG from the AmpliPi forum (white + red on transparent) traced to a
#     two-colour vector. icon_dark = as traced; icon.svg = the white text made black so it reads
#     on light; monochrome = everything white.
amp = fit_budget(
    Image.open(Path(__file__).parent / "sources" / "amplipi.png").convert("RGBA"), colours=2
)
amp_red = next(c for c in re.findall(r'fill="(#[0-9a-f]{6})"', amp) if c != "#ffffff")
write("amplipi", "icon_dark.svg", amp, "AmpliPi wordmark PNG traced to vector")
write(
    "amplipi",
    "icon.svg",
    amp.replace('fill="#ffffff"', 'fill="#000"'),
    "same vector with the white text made black",
)
write(
    "amplipi",
    "icon_monochrome.svg",
    amp.replace(f'fill="{amp_red}"', 'fill="#ffffff"'),
    "same vector, everything white",
)

# 21. itunes_podcasts, jellyfin, musicbrainz, yandex_station: monochrome = icon.svg in lifted greyscale
for domain in ("itunes_podcasts", "jellyfin", "musicbrainz", "yandex_station"):
    write(
        domain,
        "icon_monochrome.svg",
        greyscale((PROVIDERS / domain / "icon.svg").read_text()),
        "icon.svg in lifted greyscale",
    )

# 22. yandex_smarthome: icon.svg is an embedded PNG — traced to a vector (3 colours) and greyed
ys_img = png_from_svg((PROVIDERS / "yandex_smarthome" / "icon.svg").read_text())
write(
    "yandex_smarthome",
    "icon_monochrome.svg",
    greyscale(fit_budget(ys_img, colours=3)),
    "icon.svg raster traced to vector, lifted greyscale",
)

# 23. (mpd's dark variant is step 30)

# 24. radioparadise: dark variant = the icon.svg raster traced to a vector (3 colours) with the
#     black square background turned white
rp_img = png_from_svg((PROVIDERS / "radioparadise" / "icon.svg").read_text())
rp_vec = fit_budget(recolour(rp_img, dark=(255, 255, 255), threshold=40), colours=3)
write(
    "radioparadise",
    "icon_dark.svg",
    rp_vec,
    "icon.svg raster traced to vector, black background made white",
)

# 25. listenbrainz_scrobble: monochrome = the two half-hexagons white, the cream detail lines black
#     (all-white would merge the lines into the shapes)
write(
    "listenbrainz_scrobble",
    "icon_monochrome.svg",
    minify_svg(
        swap(
            (PROVIDERS / "listenbrainz_scrobble" / "icon.svg").read_text(),
            [
                ('fill="#fffedb"', 'fill="#000"'),
                ('fill="#eb743b"', 'fill="#fff"'),
                ('fill="#353070"', 'fill="#fff"'),
            ],
        ),
        decimals=2,
    ),
    "icon.svg with the shapes white and the detail lines black, minified",
)

# 26. heos: dark variant = icon.svg with the black made white; monochrome = everything white
heos = (PROVIDERS / "heos" / "icon.svg").read_text()
write(
    "heos",
    "icon_dark.svg",
    swap(heos, [('fill="#040404"', 'fill="#fff"')]),
    "icon.svg with black -> white",
)
write(
    "heos",
    "icon_monochrome.svg",
    swap(heos, [('fill="#040404"', 'fill="#fff"'), ('fill="#ca2d1a"', 'fill="#fff"')]),
    "icon.svg, everything white",
)

# 27. ai_radio, itunes_artwork: monochrome = icon.svg in lifted greyscale
for domain in ("ai_radio", "itunes_artwork"):
    write(
        domain,
        "icon_monochrome.svg",
        greyscale((PROVIDERS / domain / "icon.svg").read_text()),
        "icon.svg in lifted greyscale",
    )

# 28. ibroadcast: dark variant = icon.svg with the full-square near-black background made white
ib = (PROVIDERS / "ibroadcast" / "icon.svg").read_text()
write(
    "ibroadcast",
    "icon_dark.svg",
    swap(ib, [("fill:rgb(13.72549%,9.411765%,7.45098%)", "fill:#fff")]),
    "icon.svg with the black background made white",
)

# 29. nugs: all three from nugs.net's own logo SVG (white wordmark + purple gradient mark):
#     icon_dark as published, icon.svg with the white text made black, monochrome in greyscale
nugs = minify_svg(
    (Path(__file__).parent / "sources" / "nugs-logo-xl.svg").read_text(), decimals=2, tight=True
)
write("nugs", "icon_dark.svg", nugs, "nugs.net logo SVG, minified")
write(
    "nugs",
    "icon.svg",
    nugs.replace('fill="white"', 'fill="#000"'),
    "nugs.net logo SVG with the white text made black",
)
write("nugs", "icon_monochrome.svg", greyscale(nugs), "nugs.net logo SVG in lifted greyscale")

# 30. mpd: dark variant traced from the icon.svg raster (4 colours), dark greys lightened so the
#     mark reads on dark; the earlier copy of icon.svg was invisible there
mpd_img = png_from_svg((PROVIDERS / "mpd" / "icon.svg").read_text())
write(
    "mpd",
    "icon_dark.svg",
    lighten_dark_fills(fit_budget(mpd_img, colours=4)),
    "icon.svg raster traced to vector, dark greys lightened",
)

# monochromes the user chose to keep as they are
KEEP = {
    "builtin": "kept as-is (user)",
    "coverartarchive": "kept as-is (user)",
    "filesystem_nfs": "kept as-is (user)",
    "filesystem_smb": "kept as-is (user)",
    "webdav": "kept as-is (user)",
    "roku_media_assistant": "kept as-is (user)",
    "soundcloud": "kept as-is (user)",
    "musicme": "kept as-is (user)",
    "mpd": "kept as-is (user)",
}

for entry in done:
    domain, rest = entry.split("/", 1)
    add_note(domain, re.sub(r" \(\d+ B\)$", "", rest))
for domain, why in KEEP.items():
    add_note(domain, f"icon_monochrome.svg: {why}")

# record the monochromes this script owns so make-mono.py keeps them in the plan
plan = json.loads(PLAN.read_text()) if PLAN.exists() else {}
for domain, how in {
    "_demo_music_provider": "copy of icon_dark.svg",
    "_demo_player_provider": "copy of icon_dark.svg",
    "_demo_plugin_provider": "copy of icon_dark.svg",
    "alexa": "icon.svg, all white",
    "ariacast_receiver": "icon.svg, blues set to black (white tile kept)",
    "lastfm_recommendations": "copy of lastfm_scrobble/icon_monochrome.svg",
    "smart_playlist": "icon.svg, blue -> white, white -> black",
    "bbc_sounds": "icon.svg in lifted greyscale",
    "filesystem_onedrive": "new icon.svg in lifted greyscale",
    "lrclib": "icon.svg PNG inverted, 160 px",
    "nts": "copy of icon.svg (tile + text invert cleanly)",
    "openai_compatible": "icon.svg, purple -> white, white -> black",
    "airplay": "original icon.svg in white",
    "amplipi": "forum PNG, everything white",
    "itunes_podcasts": "icon.svg in lifted greyscale",
    "jellyfin": "icon.svg in lifted greyscale",
    "musicbrainz": "icon.svg in lifted greyscale",
    "yandex_station": "icon.svg in lifted greyscale",
    "yandex_smarthome": "icon.svg PNG in lifted greyscale",
    "listenbrainz_scrobble": "icon.svg, shapes white, detail lines black",
    "heos": "icon.svg, everything white",
    "ai_radio": "icon.svg in lifted greyscale",
    "itunes_artwork": "icon.svg in lifted greyscale",
    "nugs": "nugs.net logo SVG in lifted greyscale",
}.items():
    plan[domain] = {
        "status": plan.get(domain, {}).get("status", ""),
        "detail": "",
        "action": "manual",
        "how": how,
    }
for domain, why in KEEP.items():
    plan[domain] = {
        "status": plan.get(domain, {}).get("status", ""),
        "detail": "",
        "action": "keep",
        "how": why,
    }
PLAN.write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n")

print("\n".join(done))
