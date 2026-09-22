# ruff: noqa
"""
Build scratchpad/icon-final.html: one row per provider showing what the UI will render
once this branch lands — light theme, dark theme, monochrome on dark, monochrome on light —
with the file each cell comes from, whether that file is orig or new, and a placeholder
where the file is still to be designed.

Run from server/: python scratchpad/icon-final.py
"""

import html
from pathlib import Path

from iconlib import (
    PROVIDERS,
    all_providers,
    change_of,
    data_uri,
    icon_file,
    original_data_uri,
    pending_design,
)

OUT = Path(__file__).with_suffix(".html")
CSS: list[str] = []
PENDING_DARK, PENDING_MONO = pending_design()


def label(path: Path | None, fallback: str | None = None) -> str:
    """'icon_dark.svg · new' style caption."""
    if path is None:
        return fallback or ""
    state = {"A": "new", "M": "replaced", "": "orig"}[change_of(path)]
    return f"{path.name} &middot; {state}"


def cell(
    path: Path | None,
    surface: str,
    invert: bool = False,
    pending: str | None = None,
    caption: str | None = None,
    previous: tuple[str | None, str] | None = None,
) -> str:
    """
    One cell. `previous` is (data URI, file name) of what the UI rendered on this surface
    before the branch, when that differs from `path`; for a replaced file it defaults to the
    file's own original. The caption's state word then toggles between the two renderings.
    """
    if path is None:
        if pending:
            return f'<td class="{surface} pending"><div class="ph">DESIGN</div><small>{pending}</small></td>'
        return f'<td class="{surface} missing"><div class="ph">none</div></td>'
    uri = data_uri(path)
    name = f"i{len(CSS)}"
    CSS.append(f".{name}{{background-image:url({uri})}}")
    inv = " inv" if invert else ""
    icons = f'<span class="ic {name}{inv}"></span><span class="ic s {name}{inv}"></span>'
    text = caption or label(path)
    state = change_of(path)
    if previous is None and state == "M":
        previous = (original_data_uri(path), path.name)
    if previous and previous[0]:
        oname = f"i{len(CSS)}"
        CSS.append(f".{oname}{{background-image:url({previous[0]})}}")
        icons = (
            f'<span class="cur">{icons}</span>'
            f'<span class="old"><span class="ic {oname}{inv}"></span><span class="ic s {oname}{inv}"></span></span>'
        )
        word = "replaced" if state == "M" else "new"
        alt = f"showing {previous[1]} as before &mdash; click for {word}"
        text = text.replace(word, f'<a href="#" class="tog" data-alt="{alt}">{word}</a>', 1)
    return f'<td class="{surface}">{icons}<small>{text}</small></td>'


rows = []
for domain in all_providers():
    d = PROVIDERS / domain
    default = icon_file(d / "icon")
    dark = icon_file(d / "icon_dark")
    mono = icon_file(d / "icon_monochrome")

    # dark theme: icon_dark if it exists, else the default (that is what useProviderIcon does)
    if dark is not None:
        # a new icon_dark still displaces what dark showed before: the (original) icon.svg
        before = None
        if change_of(dark) == "A":
            before = (original_data_uri(default) or data_uri(default), default.name)
        dark_cell = cell(dark, "dark", previous=before)
    elif domain in PENDING_DARK:
        dark_cell = cell(None, "dark", pending="icon_dark.svg")
    else:
        dark_cell = cell(
            default,
            "dark",
            caption=f"{default.name} &middot; {label(default).split('&middot; ')[1]} (no icon_dark)",
        )

    mono_pending = "icon_monochrome.svg" if domain in PENDING_MONO else None
    rows.append(
        "<tr>"
        f"<th>{domain}</th>"
        + cell(default, "light")
        + dark_cell
        + cell(mono, "dark", pending=mono_pending)
        + cell(mono, "light", invert=True, pending=mono_pending)
        + "</tr>"
    )

page = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Provider icons — proposed final</title>
<style>
body{{font:14px system-ui,sans-serif;margin:16px;background:#f4f4f4;color:#222}}
table{{border-collapse:collapse}}
th,td{{border:1px solid #bbb;padding:6px 10px;text-align:center;vertical-align:middle}}
th{{text-align:left;font-weight:600}}
thead th{{position:sticky;top:0;background:#ddd}}
td.light{{background:#fff;color:#555}}
td.dark{{background:#121212;color:#999}}
td small{{display:block;font-size:11px;margin-top:4px}}
.ic{{display:inline-block;width:48px;height:48px;margin:0 6px;vertical-align:middle;background:center/contain no-repeat}}
.ic.s{{width:24px;height:24px}}
.inv{{filter:invert(1)}}
.ph{{display:inline-block;width:48px;height:48px;line-height:48px;border:2px dashed #888;border-radius:6px;font-size:10px;font-weight:700;letter-spacing:.5px}}
td.pending .ph{{border-color:#d98200;color:#d98200}}
td.missing .ph{{border-color:#e33;color:#e33}}
.old{{display:none}}
td.show-old .old{{display:inline}}
td.show-old .cur{{display:none}}
a.tog{{color:#d98200;font-weight:700;text-decoration:underline dotted;cursor:pointer}}
td.show-old a.tog{{color:#2a7bd9}}
{"".join(CSS)}
</style>
<script>
document.addEventListener("click", function (e) {{
  const a = e.target.closest("a.tog");
  if (!a) return;
  e.preventDefault();
  const td = a.closest("td");
  td.classList.toggle("show-old");
  const alt = a.dataset.alt;
  a.dataset.alt = a.textContent;
  a.textContent = alt;
}});
</script>
</head><body>
<h1>Provider icons &mdash; proposed final state (backlog#158)</h1>
<p>One row per provider ({len(rows)}). Each column is what the UI renders after this branch:
light theme shows <code>icon.svg</code>; dark theme shows <code>icon_dark.svg</code> when it exists, else <code>icon.svg</code>;
<code>icon_monochrome.svg</code> is shown as-is on dark and CSS-inverted on light.
Each cell names the file it comes from and whether that file is <b>orig</b> (shipping today, untouched),
<b style="color:#d98200">replaced</b> (existed, discarded and replaced on this branch) or <b>new</b> (there was no such file before).
Where the word is a link, click it to see what that surface showed before the branch: the original file for <b>replaced</b>,
and for a <b>new</b> <code>icon_dark.svg</code> the <code>icon.svg</code> that dark used to fall back to.
<b style="color:#d98200">DESIGN</b> = still to be produced in Claude Design; <b style="color:#e33">none</b> = no file and none planned.</p>
<table><thead>
<tr><th>provider</th><th>light theme</th><th>dark theme</th><th>monochrome on dark</th><th>monochrome on light<br>(inverted by UI)</th></tr>
</thead><tbody>
{"".join(rows)}
</tbody></table></body></html>
"""
OUT.write_text(page)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {len(rows)} rows)")
