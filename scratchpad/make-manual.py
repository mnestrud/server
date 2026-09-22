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

from iconlib import BASE, PROVIDERS, ROOT

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


def minify_svg(svg: str, decimals: int) -> str:
    """Drop editor metadata and redundant attributes, round path coordinates, collapse whitespace."""
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
}.items():
    plan[domain] = {
        "status": plan.get(domain, {}).get("status", ""),
        "detail": "",
        "action": "manual",
        "how": how,
    }
PLAN.write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n")

print("\n".join(done))
