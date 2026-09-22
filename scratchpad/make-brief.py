# ruff: noqa
"""Write scratchpad/icon-dark-brief.md for the Group B providers (Claude Design input)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / "music_assistant" / "providers"
OUT = Path(__file__).parent / "icon-dark-brief.md"
RAW = "https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers"

GROUP_B = {
    "lastfm_recommendations": "multi-colour brand mark (black + red)",
    "lastfm_scrobble": "multi-colour brand mark (black + red); same logo as lastfm_recommendations",
    "heos": "multi-colour brand mark (near-black + red)",
    "somafm": "red wordmark; no monochrome variant exists",
    "neteasecloudmusic": "dark red mark; existing monochrome is black too",
    "nugs": "red + black + white + grey mark",
    "theaudiodb": "grey #454545 body + white; decide whether to lighten the grey or go white",
    "deezer": "single brand colour #A238FF, too dark on #121212",
    "filesystem_onedrive": "single brand colour #0078D4",
    "storytel": "single brand colour #ff501c",
    "bbc_sounds": "orange tones",
    "pandora": "blue tones",
    "yandex_station": "purple-to-blue gradient",
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


sections = []
for domain, note in GROUP_B.items():
    src = PROVIDERS / domain / "icon.svg"
    text = strip_editor_noise(src.read_text(errors="replace"))
    viewbox = re.search(r'viewBox="([^"]+)"', text)
    embedded = "data:image/png" in text
    sec = [
        f"## {domain}",
        "",
        f"- why: {note}",
        f"- viewBox: `{viewbox.group(1) if viewbox else 'none'}`",
        f"- current colours: {', '.join(colours(text)) or 'n/a'}",
        f"- current size: {src.stat().st_size} B{' (embedded PNG)' if embedded else ''}",
        f"- source: {RAW}/{domain}/icon.svg",
        f"- output path: `music_assistant/providers/{domain}/icon_dark.svg`",
    ]
    mono = PROVIDERS / domain / "icon_monochrome.svg"
    if mono.exists():
        sec.append(f"- monochrome variant for reference: {RAW}/{domain}/icon_monochrome.svg")
    if not embedded and len(text) < 4000:
        sec += ["", "```svg", text.strip(), "```"]
    sections.append("\n".join(sec))

OUT.write_text(
    "\n".join(
        [
            "# Brief: icon_dark.svg for Music Assistant providers (backlog#158)",
            "",
            "Music Assistant shows each provider's logo on light and dark surfaces. Providers can ship an",
            "`icon_dark.svg` next to `icon.svg`; the UI picks it on the dark theme. The providers below have",
            "logos drawn in colours that all but disappear on a dark background. Produce one `icon_dark.svg`",
            "per provider.",
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
            *sections,
            "",
        ]
    )
)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
