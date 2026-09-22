# ruff: noqa
"""
Raster -> vector for provider icons, with potracer (pure-Python potrace).

trace_image(img, colours=N) quantises the opaque pixels to N colours, traces one layer per
colour and returns an SVG string of filled paths. Coordinates are in image pixels, rounded
to one decimal; the viewBox is the image size. fit_budget() lowers the working resolution
until the result is within the repo's 5 KB limit.
"""

import io
import re

import numpy as np
import potrace
from PIL import Image

LIMIT = 5 * 1024


def _path_d(path: potrace.Path, scale: float, decimals: int) -> str:
    def f(v: float) -> str:
        s = f"{v * scale:.{decimals}f}".rstrip("0").rstrip(".")
        return "0" if s in ("", "-0") else s

    def pt(p) -> str:  # potracer points expose .x/.y
        return f"{f(p.x)} {f(p.y)}"

    parts = []
    for curve in path:
        parts.append(f"M{pt(curve.start_point)}")
        for seg in curve.segments:
            if seg.is_corner:
                parts.append(f"L{pt(seg.c)}L{pt(seg.end_point)}")
            else:
                parts.append(f"C{pt(seg.c1)} {pt(seg.c2)} {pt(seg.end_point)}")
        parts.append("Z")
    return "".join(parts)


def _hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(int(v) for v in rgb[:3])


def trace_image(
    img: Image.Image,
    colours: int = 2,
    work_width: int | None = None,
    decimals: int = 1,
    turdsize: int = 2,
) -> str:
    """
    Trace `img` into an SVG with one filled path per colour. Transparent pixels (alpha < 128)
    are background. The output viewBox matches the original image size whatever the working
    resolution, so callers can shrink `work_width` to save bytes without changing geometry.
    """
    img = img.convert("RGBA")
    w0, h0 = img.size
    work = (
        img
        if not work_width or work_width >= w0
        else img.resize((work_width, round(h0 * work_width / w0)), Image.LANCZOS)
    )
    arr = np.asarray(work)
    alpha = arr[:, :, 3] >= 128
    # quantise the opaque pixels only (as a 1 x N strip), so transparency never takes a palette slot;
    # start with more colours than wanted, then merge similar ones so the palette holds the most
    # populous *distinct* colours (median cut alone spends every slot on shades of a dominant colour)
    opaque = arr[alpha][:, :3].astype(np.uint8)
    strip = Image.fromarray(opaque.reshape(1, -1, 3)).quantize(
        min(32, 8 * colours), method=Image.Quantize.MEDIANCUT
    )
    labels = np.asarray(strip).reshape(-1)
    raw_pal = np.array(strip.getpalette()[: 3 * (labels.max() + 1)]).reshape(-1, 3).astype(float)
    counts = np.bincount(labels, minlength=len(raw_pal))
    kept: list[int] = []
    remap = {}
    for i in np.argsort(-counts):
        if counts[i] == 0:
            continue
        near = [k for k in kept if np.linalg.norm(raw_pal[i] - raw_pal[k]) < 56]
        if near:
            remap[i] = near[0]
        elif len(kept) < colours:
            kept.append(int(i))
            remap[i] = int(i)
        else:
            remap[i] = int(min(kept, key=lambda k: np.linalg.norm(raw_pal[i] - raw_pal[k])))
    merged = np.vectorize(remap.get)(labels)
    idx = np.full(alpha.shape, -1, dtype=int)
    idx[alpha] = merged
    scale = w0 / work.size[0]
    # speckle threshold grows with the working resolution (anti-aliasing crumbs are ~1-2 px)
    turd = max(turdsize, round(work.size[0] * work.size[1] / 4000))
    min_area = max(turd * 4, int(alpha.sum() * 0.004))
    layers = []
    for i in kept:
        # population-weighted mean of the merged shades, so the layer colour is the real one
        members = [j for j, k in remap.items() if k == i]
        colour = (raw_pal[members] * counts[members][:, None]).sum(0) / counts[members].sum()
        mask = idx == i
        if mask.sum() < min_area:
            continue
        bmp = potrace.Bitmap(mask)
        path = bmp.trace(
            turdsize=turd,
            turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
            alphamax=1.0,
            opticurve=1,
            opttolerance=0.2,
        )
        d = _path_d(path, scale, decimals)
        if d:
            layers.append((int(mask.sum()), f'<path fill="{_hex(colour)}" d="{d}"/>'))
    # larger areas first so small details paint on top
    layers.sort(key=lambda t: -t[0])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w0} {h0}">'
        + "".join(p for _, p in layers)
        + "</svg>"
    )


def fit_budget(img: Image.Image, colours: int = 2, limit: int = LIMIT, **kw) -> str:
    """trace_image at decreasing working widths until the SVG fits `limit` bytes."""
    w0 = img.size[0]
    last = ""
    for width in (w0, 512, 384, 256, 192, 160, 128, 96, 64):
        if width > w0:
            continue
        last = trace_image(img, colours=colours, work_width=width, **kw)
        if len(last.encode()) <= limit:
            return last
    # last resort: integer coordinates
    last = trace_image(img, colours=colours, work_width=64, decimals=0, **kw)
    return last


def png_from_svg(svg: str) -> Image.Image:
    """The PNG embedded in an svg-wrapped raster, as a PIL image."""
    import base64
    from urllib.parse import unquote

    m = re.search(r"data:image/png;base64,((?:[A-Za-z0-9+/=%\s]|&#1[03];)+)", svg)
    raw = base64.b64decode(re.sub(r"\s|&#1[03];", "", unquote(m.group(1))))
    return Image.open(io.BytesIO(raw)).convert("RGBA")
