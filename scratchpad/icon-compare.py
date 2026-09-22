# ruff: noqa
"""
Build scratchpad/icon-compare.html: before/after review of provider icon dark variants.

Run from server/: python scratchpad/icon-compare.py
Icons are embedded as data URIs (the way the frontend serves them), so the page is
self-contained and ids inside the SVGs cannot clash.
"""

import base64
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / "music_assistant" / "providers"
OUT = Path(__file__).with_suffix(".html")
LIMIT = 5 * 1024

GROUPS = {
    "A": (
        "text edit: icon.svg with the dark colour swapped to white",
        [
            "airplay_receiver",
            "fastmcp_server",
            "nicovideo",
            "orf_radiothek",
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
            "airplay",
            "fully_kiosk",
            "siriusxm",
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


CSS: list[str] = []  # one background-image rule per icon, so each data URI appears once


def changed_files() -> dict[str, str]:
    """Provider icon files this branch adds (A) or modifies (M), relative to where it forked from dev."""
    base = subprocess.check_output(
        ["git", "merge-base", "dev", "HEAD"], cwd=ROOT, text=True
    ).strip()
    out = subprocess.check_output(
        ["git", "diff", "--name-status", base, "--", "music_assistant/providers"],
        cwd=ROOT,
        text=True,
    )
    status = {}
    for line in out.splitlines():
        code, path = line.split("\t", 1)
        status[path] = code[0]
    # uncommitted work counts too
    for line in subprocess.check_output(
        ["git", "status", "--porcelain", "--", "music_assistant/providers"], cwd=ROOT, text=True
    ).splitlines():
        code, path = line[:2].strip() or "M", line[3:]
        status.setdefault(path, "A" if code == "?" else code[0])
    return status


CHANGED = changed_files()
BADGE = {"A": '<div class="tag new">NEW</div>', "M": '<div class="tag chg">CHANGED</div>'}


def badge(path: Path) -> str:
    return BADGE.get(CHANGED.get(str(path.relative_to(ROOT)), ""), "")


def cell(uri: str | None, surface: str, path: Path | None = None, invert: bool = False) -> str:
    if uri is None:
        return f'<td class="{surface} missing">MISSING</td>'
    name = f"i{len(CSS)}"
    CSS.append(f".{name}{{background-image:url({uri})}}")
    inv = " inv" if invert else ""
    tag = badge(path) if path else ""
    return f'<td class="{surface}"><span class="ic {name}{inv}"></span><span class="ic s {name}{inv}"></span>{tag}</td>'


def size_cell(*paths: Path) -> str:
    parts = []
    for path in paths:
        if not path.exists():
            parts.append("&mdash;")
            continue
        n = path.stat().st_size
        parts.append(f'<span class="over">{n} B</span>' if n > LIMIT else f"{n} B")
    return "<td>" + "<br>".join(parts) + "</td>"


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


# monochrome work across ALL providers, from make-mono.py
plan_path = Path(__file__).parent / "mono-plan.json"
if plan_path.exists():
    plan = json.loads(plan_path.read_text())
    dark_scope = set(GROUPS["A"][1]) | set(GROUPS["B"][1])
    by_action: dict[str, list[str]] = {"derived": [], "design": [], "debt": []}
    for domain, item in sorted(plan.items()):
        if domain in dark_scope and item["action"] != "debt":
            continue  # already listed above; its monochrome is part of that row
        by_action[item["action"]].append(domain)
    GROUPS["M1"] = (
        "monochrome derived by text edit (single-colour source recoloured to white)",
        by_action["derived"],
    )
    GROUPS["M2"] = (
        "monochrome for Claude Design (multi-colour or raster source)",
        by_action["design"],
    )
    GROUPS["M3"] = (
        "monochrome debt: renders correctly but is an oversized white raster or a black+white two-tone; optional",
        by_action["debt"],
    )

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
        note = colours(d / "icon.svg")
        if plan_path.exists() and domain in plan:
            note += f"<br>mono: {html.escape(plan[domain].get('how') or plan[domain]['status'])}"
        rows.append(
            "<tr>"
            f"<th>{domain}<br><small>{note}</small></th>"
            + cell(default, "light", d / "icon.svg")
            + cell(default, "dark", d / "icon.svg")
            + cell(dark, "dark", d / "icon_dark.svg")
            + cell(mono, "dark", d / "icon_monochrome.svg")
            + cell(mono, "light", d / "icon_monochrome.svg", invert=True)
            + size_cell(d / "icon_dark.svg", d / "icon_monochrome.svg")
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
.ic{{display:inline-block;width:48px;height:48px;margin:0 6px;vertical-align:middle;background:center/contain no-repeat}}
.ic.s{{width:24px;height:24px}}
td.missing{{color:#e33;font-weight:600}}
.over{{color:#e33;font-weight:600}}
.inv{{filter:invert(1)}}
.tag{{font-size:10px;font-weight:700;letter-spacing:.5px;margin-top:4px}}
.tag.new{{color:#2a9d3f}}
.tag.chg{{color:#d98200}}
{"".join(CSS)}
</style></head><body>
<h1>backlog#158 &mdash; provider icon dark and monochrome variants</h1>
<p>Each cell shows the icon at 48px and 24px (the setup wizard badge uses 16px).
Column 2 is today's dark-theme rendering; column 3 is the new dark file.
The monochrome file must be white on transparent: the UI shows it as-is on dark (column 4)
and CSS-inverts it on light (column 5), exactly as rendered here. Sizes over 5&nbsp;KB fail the repo lint.<br>
A cell without a badge is the file shipping today; <b style="color:#2a9d3f">NEW</b> did not exist before this branch;
<b style="color:#d98200">CHANGED</b> existed and was replaced. MISSING means no file yet.</p>
<table>
<tr><th>provider</th><th>icon.svg on light</th><th>icon.svg on dark<br>(today)</th>
<th>icon_dark.svg on dark</th>
<th>icon_monochrome on dark</th><th>icon_monochrome on light<br>(inverted by the UI)</th>
<th>size<br>dark / mono</th><th>group</th></tr>
{"".join(rows)}
</table></body></html>
"""
OUT.write_text(page)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
