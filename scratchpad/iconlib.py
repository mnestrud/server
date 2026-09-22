# ruff: noqa
"""Shared bits for the review pages: provider groups, git change status, icon data URIs."""

import base64
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / "music_assistant" / "providers"
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
            "heos",
            "theaudiodb",
            "filesystem_onedrive",
            "bbc_sounds",
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
        "no icon_dark planned: readable on dark as-is, or the user chose to keep icon.svg",
        [
            "deezer",
            "lastfm_recommendations",
            "lastfm_scrobble",
            "neteasecloudmusic",
            "nugs",
            "pandora",
            "siriusxm",
            "somafm",
            "storytel",
            "yandex_station",
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


def mono_plan() -> dict:
    path = Path(__file__).parent / "mono-plan.json"
    return json.loads(path.read_text()) if path.exists() else {}


def pending_design() -> tuple[set[str], set[str]]:
    """(providers whose icon_dark.svg is still to be designed, providers whose icon_monochrome.svg is)."""
    dark = {d for d in GROUPS["B"][1] if not (PROVIDERS / d / "icon_dark.svg").exists()}
    mono = {d for d, p in mono_plan().items() if p["action"] == "design"}
    return dark, mono


def data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def icon_file(path: Path) -> Path | None:
    """The file the server would serve for this variant: svg preferred over png."""
    for suffix in (".svg", ".png"):
        if path.with_suffix(suffix).exists():
            return path.with_suffix(suffix)
    return None


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
BASE = subprocess.check_output(["git", "merge-base", "dev", "HEAD"], cwd=ROOT, text=True).strip()


def original_data_uri(path: Path) -> str | None:
    """The file as it was before this branch (from the branch base), as a data URI."""
    rel = str(path.relative_to(ROOT))
    try:
        raw = subprocess.check_output(["git", "show", f"{BASE}:{rel}"], cwd=ROOT)
    except subprocess.CalledProcessError:
        return None
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def change_of(path: Path) -> str:
    """'' for a file shipping today, 'A' for one this branch adds, 'M' for one it replaces."""
    return CHANGED.get(str(path.relative_to(ROOT)), "")


def all_providers() -> list[str]:
    return sorted(
        d.name
        for d in PROVIDERS.iterdir()
        if d.is_dir() and not d.name.startswith("__") and icon_file(d / "icon") is not None
    )
