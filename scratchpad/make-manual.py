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


def reencode_png_in_svg(svg: str, width: int, invert: bool = False) -> str:
    """Re-encode the embedded PNG at the given width as a 64-colour palette PNG; optionally invert it first."""
    m = re.search(r"data:image/png;base64,((?:[A-Za-z0-9+/=%\s]|&#1[03];)+)", svg)
    raw = base64.b64decode(re.sub(r"\s|&#1[03];", "", m.group(1)))
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    if invert:
        rgb = ImageOps.invert(img.convert("RGB"))
        img = Image.merge("RGBA", (*rgb.split(), img.getchannel("A")))
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
    svg = re.sub(
        r'\s+(id|version|xml:space|enable-background|xmlns:xlink|xmlns:svg|xmlns:sodipodi|xmlns:inkscape|inkscape:[\w-]+|sodipodi:[\w-]+)="[^"]*"',
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

# 8. msx_bridge: today's white icon.svg becomes the dark variant; icon.svg is the PNG inverted
msx = original("msx_bridge", "icon.svg").decode()
write("msx_bridge", "icon_dark.svg", msx, "the original white icon.svg")
write(
    "msx_bridge",
    "icon.svg",
    invert_png_in_svg(msx),
    "original with the embedded PNG pixel-inverted",
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

# 14. lrclib: monochrome is icon.svg with the embedded PNG inverted (re-encoded small enough
#     for the budget); the same file is the dark variant
lrc = reencode_png_in_svg(original("lrclib", "icon.svg").decode(), width=160, invert=True)
write("lrclib", "icon_monochrome.svg", lrc, "icon.svg with the PNG inverted, re-encoded at 160 px")
write("lrclib", "icon_dark.svg", lrc, "same file as icon_monochrome.svg")

# 15. musiccast: monochrome doubles as the dark variant; the 29 KB raster is re-encoded at
#     128 px so the new file fits the budget (the monochrome itself is grandfathered)
write(
    "musiccast",
    "icon_dark.svg",
    reencode_png_in_svg((PROVIDERS / "musiccast" / "icon_monochrome.svg").read_text(), width=128),
    "icon_monochrome.svg re-encoded at 128 px",
)

# 16. musicme: monochrome doubles as the dark variant
write(
    "musicme",
    "icon_dark.svg",
    (PROVIDERS / "musicme" / "icon_monochrome.svg").read_text(),
    "copy of icon_monochrome.svg",
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

for entry in done:
    domain, rest = entry.split("/", 1)
    add_note(domain, re.sub(r" \(\d+ B\)$", "", rest))

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
}.items():
    plan[domain] = {
        "status": plan.get(domain, {}).get("status", ""),
        "detail": "",
        "action": "manual",
        "how": how,
    }
PLAN.write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n")

print("\n".join(done))
