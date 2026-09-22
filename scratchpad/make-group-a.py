# ruff: noqa
"""Write icon_dark.svg for the Group A providers: icon.svg with the dark colour swapped."""

from pathlib import Path

PROVIDERS = Path("/home/ataraxia/code/music-assistant/server/music_assistant/providers")

# domain -> list of (old, new) replacements applied to icon.svg
SWAPS = {
    "wikipedia": [("<path d=", '<path fill="#fff" d=')],
    "airplay": [("fill:#0000ff", "fill:#fff")],
    "airplay_receiver": [('fill="currentColor"', 'fill="#fff"')],
    "orf_radiothek": [('fill="currentColor"', 'fill="#fff"')],
    "siriusxm": [("fill: #0000eb", "fill: #fff")],
    "fully_kiosk": [("fill:#00f;", "fill:#fff;")],
    "nicovideo": [('fill="#000"', 'fill="#fff"')],
    "fastmcp_server": [('stroke="black"', 'stroke="white"')],
}
# black tile + white bars -> white tile + black bars (samsung_wam precedent)
for demo in ("_demo_music_provider", "_demo_player_provider", "_demo_plugin_provider", "test"):
    SWAPS[demo] = [
        ("fill:rgb(0%,0%,0%)", "fill:__DARK__"),
        ("fill:rgb(100%,100%,100%)", "fill:rgb(0%,0%,0%)"),
        ("fill:__DARK__", "fill:rgb(100%,100%,100%)"),
    ]

for domain, swaps in SWAPS.items():
    src = PROVIDERS / domain / "icon.svg"
    dst = PROVIDERS / domain / "icon_dark.svg"
    text = src.read_text()
    for old, new in swaps:
        assert old in text, f"{domain}: {old!r} not found"
        text = text.replace(old, new)
    assert text != src.read_text(), f"{domain}: unchanged"
    dst.write_text(text)
    print(f"{domain:24s} {dst.stat().st_size:5d} B")
