# ruff: noqa
"""
Build scratchpad/icon-compare.html: before/after review of provider icon dark variants.

Run from server/: python scratchpad/icon-compare.py
Icons are embedded as data URIs (the way the frontend serves them), so the page is
self-contained and ids inside the SVGs cannot clash.
"""

import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / "music_assistant" / "providers"
OUT = Path(__file__).with_suffix(".html")
LIMIT = 5 * 1024

GROUPS = {
    "A": (
        "text edit: icon.svg with the dark colour swapped to white",
        [
            "airplay",
            "airplay_receiver",
            "fastmcp_server",
            "fully_kiosk",
            "nicovideo",
            "orf_radiothek",
            "siriusxm",
            "wikipedia",
            "_demo_music_provider",
            "_demo_player_provider",
            "_demo_plugin_provider",
            "test",
        ],
    ),
    "B": (
        "Claude Design: multi-colour brand mark, brand colour too dark, or embedded PNG",
        [
            "lastfm_recommendations",
            "lastfm_scrobble",
            "heos",
            "somafm",
            "neteasecloudmusic",
            "nugs",
            "theaudiodb",
            "deezer",
            "filesystem_onedrive",
            "storytel",
            "bbc_sounds",
            "pandora",
            "yandex_station",
            "ibroadcast",
            "gpodder",
            "lrclib",
            "musicme",
            "internet_archive",
            "radioparadise",
            "musiccast",
            "mpd",
        ],
    ),
    "skip": (
        "no file planned: readable on dark as-is (black tile vanishes, light glyph stays)",
        [
            "abc_radio_network",
            "amplipi",
            "apple_music",
            "bluesound",
            "nts",
            "podcastfeed",
            "ariacast_receiver",
            "sonos",
            "chromecast",
        ],
    ),
}


def data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def icon(path: Path) -> str | None:
    """Prefer svg, fall back to png, like detect_provider_icons."""
    return data_uri(path.with_suffix(".svg")) or data_uri(path.with_suffix(".png"))


def cell(uri: str | None, surface: str) -> str:
    if uri is None:
        return f'<td class="{surface} missing">MISSING</td>'
    return (
        f'<td class="{surface}"><img src="{uri}" width="48" height="48">'
        f'<img src="{uri}" width="24" height="24"></td>'
    )


def size_cell(path: Path) -> str:
    if not path.exists():
        return "<td>&mdash;</td>"
    n = path.stat().st_size
    cls = ' class="over"' if n > LIMIT else ""
    return f"<td{cls}>{n} B</td>"


def colours(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(errors="replace")
    text = re.sub(r"<sodipodi:namedview.*?/>|<metadata>.*?</metadata>", "", text, flags=re.DOTALL)
    found = set(re.findall(r"(?:fill|stroke|stop-color)\s*[:=]\s*\"?\s*([#\w]+)", text))
    found -= {"none", "evenodd", "nonzero"}
    if "data:image/png" in text:
        found.add("embedded-png")
    return ", ".join(sorted(found))


rows = []
for group, (desc, domains) in GROUPS.items():
    rows.append(
        f'<tr class="group"><th colspan="8">Group {group} &mdash; {html.escape(desc)}</th></tr>'
    )
    for domain in domains:
        d = PROVIDERS / domain
        default = icon(d / "icon")
        dark = icon(d / "icon_dark")
        mono = icon(d / "icon_monochrome")
        rows.append(
            "<tr>"
            f"<th>{domain}<br><small>{html.escape(colours(d / 'icon.svg'))}</small></th>"
            + cell(default, "light")
            + cell(default, "dark")
            + cell(dark, "dark")
            + cell(dark, "light")
            + (cell(mono, "dark") if mono else '<td class="dark none">none</td>')
            + size_cell(d / "icon_dark.svg")
            + f"<td>{group}</td></tr>"
        )

page = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Provider icon dark variants</title>
<style>
body{{font:14px system-ui,sans-serif;margin:16px;background:#f4f4f4;color:#222}}
table{{border-collapse:collapse}}
th,td{{border:1px solid #bbb;padding:6px 10px;text-align:center;vertical-align:middle}}
th{{text-align:left;font-weight:600}}
th small{{font-weight:400;color:#666}}
tr.group th{{background:#ddd;text-align:left}}
td.light{{background:#fff}}
td.dark{{background:#121212;color:#888}}
td img{{vertical-align:middle;margin:0 6px}}
td.missing{{color:#e33;font-weight:600}}
td.over{{color:#e33;font-weight:600}}
</style></head><body>
<h1>backlog#158 &mdash; provider icon dark variants</h1>
<p>Each cell shows the icon at 48px and 24px (the setup wizard badge uses 16px).
Column 2 is today's dark-theme rendering; column 3 is the new file. Sizes over 5&nbsp;KB fail the repo lint.</p>
<table>
<tr><th>provider</th><th>icon.svg on light</th><th>icon.svg on dark<br>(today)</th>
<th>icon_dark.svg on dark<br>(new)</th><th>icon_dark.svg on light<br>(sanity)</th>
<th>icon_monochrome on dark</th><th>icon_dark size</th><th>group</th></tr>
{"".join(rows)}
</table></body></html>
"""
OUT.write_text(page)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
