# ruff: noqa
"""Write scratchpad/icon-dark-brief.md for the Group B providers (Claude Design input)."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / "music_assistant" / "providers"
OUT = Path(__file__).parent / "icon-dark-brief.md"
RAW = "https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers"

GROUP_B = {
    "airplay": "single-colour #0000ff mark; brand mark, not a plain glyph",
    "fully_kiosk": "single-colour #00f mark; brand mark, not a plain glyph",
    "heos": "multi-colour brand mark (near-black + red)",
    "theaudiodb": "grey #454545 body + white; decide whether to lighten the grey or go white",
    "filesystem_onedrive": "single brand colour #0078D4",
    "bbc_sounds": "orange tones",
    "ibroadcast": "dark brown + greys",
    "gpodder": "dark grey + purple + white",
    "lrclib": "embedded PNG, mostly near-black: needs re-drawing as a vector",
    "musicme": "embedded PNG, dark: needs re-drawing as a vector",
    "internet_archive": "embedded PNG, near-black: needs re-drawing as a vector",
    "radioparadise": "embedded PNG, dark: needs re-drawing as a vector",
    "musiccast": "embedded PNG, dark: needs re-drawing as a vector",
    "mpd": "embedded PNG, mid-dark: needs re-drawing as a vector",
}


def strip_editor_noise(text: str) -> str:
    text = re.sub(r"<sodipodi:namedview.*?/>", "", text, flags=re.DOTALL)
    text = re.sub(r"<metadata>.*?</metadata>", "", text, flags=re.DOTALL)
    return text


def colours(text: str) -> list[str]:
    found = set(re.findall(r"(?:fill|stroke|stop-color)\s*[:=]\s*\"?\s*([#\w]+)", text))
    return sorted(found - {"none", "evenodd", "nonzero"})


def mono_status(path: Path) -> str:
    """Why the existing monochrome file (if any) needs replacing."""
    if not path.exists():
        return "none exists: create one"
    text = strip_editor_noise(path.read_text(errors="replace"))
    size = path.stat().st_size
    if "data:image/png" in text:
        return f"exists but is an embedded PNG ({size} B): replace with a vector"
    cols = colours(text)
    white = {"#fff", "#ffffff", "#FFF", "#FFFFFF", "white"}
    if set(cols) <= white and size <= 5 * 1024:
        return f"exists and is fine (white, {size} B): keep it"
    if set(cols) <= white:
        return f"exists, white but {size} B (over 5 KB): simplify it"
    return f"exists but uses {', '.join(cols)}: replace, must be white only"


# owner-published assets worth reusing (see logo-research.md for the full survey)
RESEARCH = {
    "wikipedia": "official white mono globe exists: https://upload.wikimedia.org/wikipedia/commons/f/fe/Wikipedia-logo-v2-bw_%28White%29.svg (CC BY-SA); our W recolour already matches",
    "internet_archive": "official colour-agnostic glyph: https://raw.githubusercontent.com/internetarchive/ia-icons/master/svg/ia-logo.svg (AGPL-3.0 repo) — recolour that rather than redraw",
    "ibroadcast": "official dark 'Powered by' SVG (multi-grey, no modification allowed): https://help.ibroadcast.com/ibroadcast-dark-compact-powered.svg — candidate for icon_dark; monochrome must still be white",
    "fastmcp_server": "official favicon-dark.svg in the repo (Apache-2.0): https://raw.githubusercontent.com/jlowin/fastmcp/main/docs/assets/brand/favicon-dark.svg",
    "airplay": "Apple HIG says use the white AirPlay icon on dark backgrounds; glyph shipped only as PDF in a .dmg — a white recolour of our mark is the same thing",
    "deezer": "brand rule: logo is white on dark / black on light; press-kit zip may hold the white file: https://newsroom-deezer.com/wp-content/uploads/2025/07/DEEZER-LOGO.zip",
    "somafm": "owner allows black or white for B/W use depending on background (https://somafm.com/linktous/logos.html); vector only as EPS",
    "theaudiodb": "site header SVG is white + blue, suited to dark: https://www.theaudiodb.com/images/logo_simple.svg (8.5 KB, site asset)",
    "nugs": "site SVG logo is white + gradient: https://cdn.nugsdev.net/images/logo-xl.svg (site asset, not a published download)",
    "radioparadise": "single-colour sigil mask exists: https://radioparadise.com/safari-pinned-tab.svg (#000, recolour to white)",
    "bbc_sounds": "BBC requires written consent for any logo use; no assets published",
    "filesystem_onedrive": "Microsoft: icon must be used in full colour; no white variant public",
    "musiccast": "Yamaha: logos only on request (requestforlogos@yamaha.com)",
    "yandex_station": "Yandex: white badge exists but gated to certified devices",
}

sections = []
for domain, note in GROUP_B.items():
    src = PROVIDERS / domain / "icon.svg"
    text = strip_editor_noise(src.read_text(errors="replace"))
    viewbox = re.search(r'viewBox="([^"]+)"', text)
    embedded = "data:image/png" in text
    mono = PROVIDERS / domain / "icon_monochrome.svg"
    sec = [
        f"## {domain}",
        "",
        f"- why: {note}",
        f"- viewBox: `{viewbox.group(1) if viewbox else 'none'}`",
        f"- current colours: {', '.join(colours(text)) or 'n/a'}",
        f"- current size: {src.stat().st_size} B{' (embedded PNG)' if embedded else ''}",
        f"- source: {RAW}/{domain}/icon.svg",
        f"- output 1: `music_assistant/providers/{domain}/icon_dark.svg`",
        f"- output 2: `music_assistant/providers/{domain}/icon_monochrome.svg` — {mono_status(mono)}",
    ]
    if mono.exists():
        sec.append(f"- current monochrome file: {RAW}/{domain}/icon_monochrome.svg")
    if domain in RESEARCH:
        sec.append(f"- official assets: {RESEARCH[domain]}")
    if not embedded and len(text) < 4000:
        sec += ["", "```svg", text.strip(), "```"]
    sections.append("\n".join(sec))

# monochrome-only work: providers whose dark icon is fine but whose monochrome needs drawing
mono_sections = []
plan_path = Path(__file__).parent / "mono-plan.json"
if plan_path.exists():
    plan = json.loads(plan_path.read_text())
    mono_sections.append("# Part 2 — monochrome only")
    mono_sections.append("")
    mono_sections.append(
        "These providers keep their icon.svg and need only `icon_monochrome.svg`: pure white on transparent, "
        "vector, <= 5 KB, same viewBox as icon.svg. The current file (if any) is unusable for the reason given."
    )
    for domain, item in sorted(plan.items()):
        if item["action"] != "design" or domain in GROUP_B:
            continue
        src = PROVIDERS / domain / "icon.svg"
        text = strip_editor_noise(src.read_text(errors="replace")) if src.exists() else ""
        viewbox = re.search(r'viewBox="([^"]+)"', text)
        sec = [
            "",
            f"## {domain}",
            "",
            f"- current monochrome: {item['status']} — {item['detail'] or 'none'}",
            f"- viewBox: `{viewbox.group(1) if viewbox else 'none'}`",
            f"- icon colours: {', '.join(colours(text)) or 'n/a'}",
            f"- source: {RAW}/{domain}/icon.svg",
            f"- output: `music_assistant/providers/{domain}/icon_monochrome.svg`",
        ]
        if domain in RESEARCH:
            sec.append(f"- official assets: {RESEARCH[domain]}")
        mono_sections += sec

OUT.write_text(
    "\n".join(
        [
            "# Brief: icon_dark.svg for Music Assistant providers (backlog#158)",
            "",
            "Music Assistant shows each provider's logo on light and dark surfaces. Providers can ship an",
            "`icon_dark.svg` next to `icon.svg`; the UI picks it on the dark theme. The providers below have",
            "logos drawn in colours that all but disappear on a dark background. Produce, per provider:",
            "",
            "1. `icon_dark.svg` — the logo for dark surfaces: white, or a lightened brand colour; may keep",
            "   several colours.",
            "2. `icon_monochrome.svg` — a single-colour version, **pure white (`#fff`) on transparent**, no",
            "   other colours, no greys, no opacity tricks. The UI shows it as-is on dark surfaces and",
            "   CSS-inverts it (`filter: invert(1)`) on light ones, so anything that is not white breaks.",
            "   Skip it only where the per-provider entry says the existing one is fine.",
            "",
            "## Rules for every file",
            "",
            "- Same `viewBox` as the source `icon.svg`; same geometry wherever the source is a vector",
            "  (the existing 20 dark variants in the repo are the default file with black swapped to white).",
            "- Plain vector SVG, **5 KB or less** (repo lint fails above that). No embedded raster images,",
            "  no editor metadata (`sodipodi`, `inkscape`, `metadata`), no `<text>` (fonts are not available).",
            "- Transparent background. Must read clearly on `#121212` at 16 px, 24 px and 48 px.",
            "- No `currentColor` and no CSS variables: the file is served as a `data:` URI, so those resolve",
            "  to black. Use literal colours.",
            "- Keep the brand's identity: white or a lightened brand colour, not a redesign.",
            "- Filename `icon_dark.svg`; drop it in the output path given per provider.",
            "",
            "Review page with today's rendering on dark for each provider:",
            "https://htmlpreview.github.io/?https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/scratchpad/icon-compare.html",
            "",
            "Survey of owner-published assets (what can be reused instead of redrawn): "
            "https://github.com/mnestrud/server/blob/review/provider-dark-icons/scratchpad/logo-research.md",
            "",
            "# Part 1 — dark + monochrome",
            "",
            *sections,
            "",
            *mono_sections,
            "",
        ]
    )
)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
