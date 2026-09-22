# ruff: noqa
"""
Generate icon_monochrome.svg wherever it can be derived mechanically.

For every provider whose monochrome is missing or wrong (see mono_audit.py):
- if icon_dark.svg exists and is a white single-colour vector: copy it
- elif icon.svg (or icon_dark.svg) is a vector drawn in exactly one colour: copy with that
  colour replaced by #fff
- else: leave it for design and print why

Run from server/: .venv/bin/python scratchpad/make-mono.py [--dry-run]
"""

import json
import re
import sys
from pathlib import Path

from iconlib import change_of
from mono_audit import PROVIDERS, _colours, _strip, audit, is_white

DRY = "--dry-run" in sys.argv
COLOUR_RE = r"(?P<key>fill|stroke|stop-color)(?P<sep>\s*[:=]\s*\"?\s*)(?P<val>{})"


def single_colour_sources(domain: str):
    """Yield (file, colour) for each vector drawn in one colour; colour None means 'unfilled' (default black)."""
    # an existing monochrome drawn in the wrong single colour is the best source: right shape already
    for name in ("icon_monochrome.svg", "icon_dark.svg", "icon.svg"):
        path = PROVIDERS / domain / name
        if not path.exists():
            continue
        text = _strip(path.read_text(errors="replace"))
        if "data:image/png" in text or "<text" in text:
            continue
        cols = _colours(text)
        if len(cols) == 1:
            yield path, next(iter(cols))
        elif not cols and re.search(r"<(path|rect|circle|ellipse|polygon)\b", text):
            yield path, None


def derive(domain: str) -> str:
    dst = PROVIDERS / domain / "icon_monochrome.svg"
    too_big = []
    for path, colour in single_colour_sources(domain):
        text = _strip(path.read_text(errors="replace"))
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        text = re.sub(r"\n\s*\n", "\n", text)
        if colour is None:
            text = text.replace("<svg", '<svg fill="#fff"', 1)
            how = f"{path.name}: no fill -> #fff on <svg>"
        elif is_white(colour) and colour != "currentcolor":
            how = f"{path.name}: already white, copied"
        else:
            text = re.sub(
                COLOUR_RE.format(re.escape(colour)),
                r"\g<key>\g<sep>#fff",
                text,
                flags=re.IGNORECASE,
            )
            how = f"{path.name}: {colour} -> #fff"
        if len(text.encode()) > 5 * 1024:
            too_big.append(f"{path.name} {len(text.encode())} B")
            continue
        if not DRY:
            dst.write_text(text)
        return how
    return "design" + (
        f" (single-colour source over 5 KB: {', '.join(too_big)})" if too_big else ""
    )


if __name__ == "__main__":
    before = audit()
    plan_path = Path(__file__).parent / "mono-plan.json"
    # keep what earlier runs derived: those files now audit as "ok" but are still our changes
    previous = json.loads(plan_path.read_text()) if plan_path.exists() else {}
    # ... but only while the file is still ours (a derivation reverted to the original drops out)
    plan: dict[str, dict[str, str]] = {
        d: p
        for d, p in previous.items()
        if p["action"] in ("derived", "manual")
        and before.get(d, ("",))[0] in ("ok", "bw")
        and change_of(PROVIDERS / d / "icon_monochrome.svg")
    }
    for domain, (status, detail) in sorted(before.items()):
        if status == "ok" or domain in plan:
            continue
        if status in ("png-white", "bw"):
            plan[domain] = {"status": status, "detail": detail, "action": "debt"}
            continue
        result = derive(domain)
        plan[domain] = {
            "status": status,
            "detail": detail,
            "action": "design" if result.startswith("design") else "derived",
            "how": result,
        }
        print(f"{domain:26s} {status:9s} -> {result}")
    counts = {
        a: sum(1 for p in plan.values() if p["action"] == a) for a in ("derived", "design", "debt")
    }
    print(f"\n{counts}")
    print("design: " + ", ".join(d for d, p in sorted(plan.items()) if p["action"] == "design"))
    if not DRY:
        json.dump(plan, open(plan_path, "w"), indent=1, sort_keys=True)
