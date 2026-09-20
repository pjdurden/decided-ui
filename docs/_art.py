#!/usr/bin/env python3
"""Generate the site's artwork.

A smooth procedural field of gaussian blobs, thresholded through an 8x8 Bayer
matrix into two flat colours. Everything here is generated; no external image
is traced, sampled or embedded. Regenerate with:

    python3 docs/_art.py
"""
import math
import pathlib
from PIL import Image

OUT = pathlib.Path(__file__).parent / "img"


def bayer(n=8):
    m, size = [[0]], 1
    while size < n:
        new = [[0] * (size * 2) for _ in range(size * 2)]
        for y in range(size):
            for x in range(size):
                v = m[y][x] * 4
                new[y][x], new[y][x + size] = v, v + 2
                new[y + size][x], new[y + size][x + size] = v + 3, v + 1
        m, size = new, size * 2
    return [[v / (size * size) for v in row] for row in m]


B = bayer(8)


def render(w, h, blobs, fg, bg, path, floor=0.0):
    f = [[floor] * w for _ in range(h)]
    for cx, cy, r, amp in blobs:
        cx, cy, r = cx * w, cy * h, r * w
        for y in range(max(0, int(cy - r * 3)), min(h, int(cy + r * 3))):
            dy = (y - cy) / r
            row = f[y]
            for x in range(max(0, int(cx - r * 3)), min(w, int(cx + r * 3))):
                dx = (x - cx) / r
                row[x] += amp * math.exp(-(dx * dx + dy * dy))
    im = Image.new("RGB", (w, h), bg)
    pix = im.load()
    for y in range(h):
        row, brow = f[y], B[y & 7]
        for x in range(w):
            if row[x] > brow[x & 7]:
                pix[x, y] = fg
    im.save(OUT / path, optimize=True)
    return path


VERM = (255, 74, 30)
BONE = (250, 247, 242)
INK = (18, 17, 16)

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    render(1600, 720,
           [(0.14, 0.68, 0.11, 0.62), (0.30, 0.42, 0.09, 0.50),
            (0.46, 0.74, 0.13, 0.58), (0.62, 0.36, 0.10, 0.54),
            (0.78, 0.70, 0.12, 0.60), (0.92, 0.46, 0.09, 0.48),
            (0.22, 0.90, 0.10, 0.46), (0.70, 0.94, 0.11, 0.44)],
           VERM, BONE, "field-hero.png", floor=0.06)
    render(1600, 300,
           [(0.18, 0.55, 0.10, 0.55), (0.44, 0.40, 0.09, 0.48),
            (0.68, 0.60, 0.11, 0.52), (0.90, 0.45, 0.08, 0.44)],
           BONE, VERM, "field-band.png", floor=0.04)
    print("wrote field-hero.png and field-band.png")
