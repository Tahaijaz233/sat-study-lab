#!/usr/bin/env python3
"""Generate app/static/favicon.png and app/static/favicon.ico for SAT Study Lab.

Draws a flat, modern graduation-cap icon (indigo -> violet gradient rounded
square with a white mortarboard) and exports:
  * favicon.png   (512x512, also used by <link rel="icon">)
  * favicon.ico   (multi-size 16/32/48/64/128/256, classic .ico format)

Run from the repo root:  python scripts/make_favicon.py
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFilter

OUT_PNG = os.path.join("app", "static", "favicon.png")
OUT_ICO = os.path.join("app", "static", "favicon.ico")

SIZE = 512
TOP = (79, 70, 229)      # indigo-600  #4f46e5
BOTTOM = (124, 58, 237)  # violet-600  #7c3aed
WHITE = (255, 255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rounded_rect_gradient(size, radius, top, bottom):
    """Rounded-square canvas with a vertical gradient, RGBA."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    for y in range(size):
        t = y / (size - 1)
        color = lerp(top, bottom, t) + (255,)
        for x in range(size):
            px[x, y] = color
    img.putalpha(mask)
    return img


def draw_mortarboard(draw, cx, top_y, w, h):
    """White graduation cap centered at (cx, top_y) with size w x h."""
    # Tassel (drawn first so the board covers its top end)
    tassel_x = cx + int(w * 0.30)
    tassel_y = top_y + int(h * 0.46)
    draw.line(
        [(tassel_x, tassel_y), (tassel_x + int(w * 0.28), tassel_y + int(h * 0.62))],
        fill=WHITE, width=max(3, int(w * 0.02)),
    )
    bob_r = max(4, int(w * 0.035))
    draw.ellipse(
        [
            tassel_x + int(w * 0.28) - bob_r,
            tassel_y + int(h * 0.62) - bob_r,
            tassel_x + int(w * 0.28) + bob_r,
            tassel_y + int(h * 0.62) + bob_r,
        ],
        fill=WHITE,
    )
    # Diagonal band under the board
    band_w = int(w * 0.62)
    band_h = int(h * 0.14)
    band_y = top_y + int(h * 0.66)
    draw.polygon(
        [
            (cx - band_w // 2, band_y),
            (cx + band_w // 2, band_y),
            (cx + band_w // 2 - int(w * 0.10), band_y + band_h),
            (cx - band_w // 2 - int(w * 0.10), band_y + band_h),
        ],
        fill=WHITE,
    )
    # Board (slanted rhombus / parallelogram)
    slant = int(w * 0.16)
    draw.polygon(
        [
            (cx - w // 2 + slant, top_y),
            (cx + w // 2, top_y),
            (cx + w // 2 - slant, top_y + int(h * 0.34)),
            (cx - w // 2, top_y + int(h * 0.34)),
        ],
        fill=WHITE,
    )


def make_icon(size=512):
    img = rounded_rect_gradient(size, radius=int(size * 0.22), top=TOP, bottom=BOTTOM)

    # Soft drop shadow behind the cap
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    cx = size // 2
    draw_mortarboard(sdraw, cx, int(size * 0.37), int(size * 0.58), int(size * 0.46))
    shadow = shadow.filter(ImageFilter.BoxBlur(8))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)
    draw_mortarboard(draw, cx, int(size * 0.34), int(size * 0.58), int(size * 0.46))
    return img


def main():
    icon = make_icon(SIZE)
    os.makedirs(os.path.dirname(OUT_PNG) or ".", exist_ok=True)
    icon.save(OUT_PNG)
    icon.resize((256, 256), Image.LANCZOS).save(
        OUT_ICO,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Wrote {OUT_PNG} and {OUT_ICO}")


if __name__ == "__main__":
    sys.exit(main())
