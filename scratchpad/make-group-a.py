# ruff: noqa
"""Write icon_dark.svg for the Group A providers: icon.svg with the dark colour swapped."""

from pathlib import Path

from iconlib import add_note

PROVIDERS = Path("/home/ataraxia/code/music-assistant/server/music_assistant/providers")

# domain -> list of (old, new) replacements applied to icon.svg
SWAPS = {
    "wikipedia": [("<path d=", '<path fill="#fff" d=')],
    "airplay_receiver": [('fill="currentColor"', 'fill="#fff"')],
    "orf_radiothek": [('fill="currentColor"', 'fill="#fff"')],
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

# monochrome must be white on transparent: the frontend shows it as-is on the dark theme
# and CSS-inverts it on the light theme. For a single-colour glyph it equals the dark file.
# The demo/test tile + bars boilerplate: monochrome is the dark file too (user's call).
MONO = {
    "wikipedia": SWAPS["wikipedia"],
    "airplay_receiver": SWAPS["airplay_receiver"],
    "orf_radiothek": SWAPS["orf_radiothek"],
    "nicovideo": SWAPS["nicovideo"],
    "fastmcp_server": SWAPS["fastmcp_server"],
}
# (test keeps the white-bars monochrome from the first pass; the user named only the demos)
for demo in ("_demo_music_provider", "_demo_player_provider", "_demo_plugin_provider"):
    MONO[demo] = SWAPS[demo]


def write_variant(domain: str, name: str, swaps: list[tuple[str, str]]) -> None:
    src = PROVIDERS / domain / "icon.svg"
    dst = PROVIDERS / domain / name
    text = src.read_text()
    for old, new in swaps:
        assert old in text, f"{domain}: {old!r} not found"
        text = text.replace(old, new)
    assert text != src.read_text(), f"{domain}: unchanged"
    dst.write_text(text)
    add_note(
        domain,
        f"{name}: icon.svg with {'colours swapped' if 'rgb(' in swaps[0][0] else 'the colour set to white'}",
    )
    print(f"{domain:24s} {name:20s} {dst.stat().st_size:5d} B")


for domain, swaps in SWAPS.items():
    write_variant(domain, "icon_dark.svg", swaps)
for domain, swaps in MONO.items():
    write_variant(domain, "icon_monochrome.svg", swaps)
