#!/usr/bin/env python3
"""Generate assets/logo.svg and a 1024x1024 opaque assets/logo.png."""

from __future__ import annotations

import math
import sys
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_PATH = Path(
    "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
)

BG = "#0D2428"
FG = "#F4F0E6"
MINT = "#5EE6A8"
SIZE = 1024


def rel_lum(hex_color: str) -> float:
    def chan(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(a: str, b: str) -> float:
    lighter, darker = max(rel_lum(a), rel_lum(b)), min(rel_lum(a), rel_lum(b))
    return (lighter + 0.05) / (darker + 0.05)


def wordmark_paths(text: str, font_size: float, tracking: float) -> tuple[list[str], float, float]:
    """Return SVG path ds, total width, and cap-height-ish height for Inter 800."""
    font = instantiateVariableFont(TTFont(FONT_PATH), {"wght": 800, "opsz": 48}, inplace=False)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    scale = font_size / upem
    # Inter typoAscender / typoDescender if available
    os2 = font["OS/2"]
    asc = os2.sTypoAscender * scale
    desc = os2.sTypoDescender * scale  # negative

    x = 0.0
    paths: list[str] = []
    for i, ch in enumerate(text):
        gname = cmap[ord(ch)]
        glyph = glyph_set[gname]
        pen = SVGPathPen(glyph_set)
        # Font space: y up, origin at baseline. SVG: y down.
        # Place baseline at y=0, then we'll translate in the SVG.
        tpen = type("T", (), {})  # placeholder to use TransformPen
        from fontTools.pens.transformPen import TransformPen

        tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0))
        glyph.draw(tpen)
        paths.append(pen.getCommands())
        x += glyph.width * scale
        if i < len(text) - 1:
            x += tracking
    height = asc - desc
    return paths, x, height, asc


def build_svg() -> str:
    # Wordmark
    paths, wm_w, wm_h, wm_asc = wordmark_paths("A11y", font_size=132, tracking=6)

    # Layout
    ring_cx, ring_cy = 512, 428
    ring_size = 620
    ring_r = ring_size / 2
    ring_stroke = 34
    ring_rx = 108
    ring_x = ring_cx - ring_r
    ring_y = ring_cy - ring_r

    # Wordmark centered under the ring
    gap = 48
    wm_baseline_y = ring_y + ring_size + gap + wm_asc
    wm_x = (SIZE - wm_w) / 2

    wordmark = "\n".join(
        f'    <path d="{d}" fill="{FG}"/>' for d in paths
    )

    # Person figure (geometric, original — not the ISA wheelchair symbol)
    # Head, torso, slightly raised arms, slightly open legs.
    person = f"""    <g fill="{FG}">
      <circle cx="512" cy="286" r="52"/>
      <rect x="484" y="342" width="56" height="148" rx="28"/>
      <rect x="394" y="360" width="118" height="38" rx="19" transform="rotate(-30 478 379)"/>
      <rect x="512" y="360" width="118" height="38" rx="19" transform="rotate(30 546 379)"/>
      <rect x="466" y="448" width="38" height="154" rx="19" transform="rotate(14 485 448)"/>
      <rect x="520" y="448" width="38" height="154" rx="19" transform="rotate(-14 539 448)"/>
    </g>"""

    # Verification badge overlapping the lower-right of the focus ring
    badge_cx, badge_cy, badge_r = 710, 642, 98
    # Check inside the badge (coordinates relative to badge center)
    # A crisp rounded check: left (cx-36, cy+4) -> (cx-10, cy+32) -> (cx+38, cy-28)
    check_d = (
        f"M {badge_cx - 38} {badge_cy + 6} "
        f"L {badge_cx - 8} {badge_cy + 36} "
        f"L {badge_cx + 42} {badge_cy - 30}"
    )

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}" role="img" aria-labelledby="logo-title logo-desc">
  <title id="logo-title">ADA Compliance Master</title>
  <desc id="logo-desc">A standing person inside a keyboard focus ring, marked with a check, and the word A11y, on a solid dark teal square.</desc>
  <rect width="{SIZE}" height="{SIZE}" fill="{BG}"/>
  <rect x="{ring_x}" y="{ring_y}" width="{ring_size}" height="{ring_size}" rx="{ring_rx}" ry="{ring_rx}" fill="none" stroke="{FG}" stroke-width="{ring_stroke}"/>
{person}
  <circle cx="{badge_cx}" cy="{badge_cy}" r="{badge_r + 14}" fill="{BG}"/>
  <circle cx="{badge_cx}" cy="{badge_cy}" r="{badge_r}" fill="{MINT}"/>
  <path d="{check_d}" fill="none" stroke="{BG}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/>
  <g transform="translate({wm_x:.2f} {wm_baseline_y:.2f})">
{wordmark}
  </g>
</svg>
'''
    return svg


def render_png(svg_path: Path, png_path: Path) -> None:
    svg_text = svg_path.read_text(encoding="utf-8")
    # Strip XML declaration for inline HTML
    inline = svg_text.split("?>", 1)[-1].strip() if svg_text.startswith("<?xml") else svg_text
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <style>
    html, body {{ margin: 0; padding: 0; width: {SIZE}px; height: {SIZE}px; overflow: hidden; background: {BG}; }}
    svg {{ display: block; width: {SIZE}px; height: {SIZE}px; }}
  </style>
</head>
<body>{inline}</body>
</html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": SIZE, "height": SIZE}, device_scale_factor=1)
        page.set_content(html, wait_until="load")
        page.locator("svg").first.screenshot(path=str(png_path), type="png", omit_background=False)
        browser.close()


def assert_png(png_path: Path) -> None:
    im = Image.open(png_path)
    if im.size != (SIZE, SIZE):
        raise SystemExit(f"PNG size {im.size}, expected {SIZE}x{SIZE}")
    if im.mode == "RGBA":
        alphas = {px[3] for px in im.getdata()}
        if alphas != {255}:
            raise SystemExit(f"PNG is not fully opaque; unique alpha values: {sorted(alphas)[:8]}...")
        # Flatten check already opaque
    elif im.mode != "RGB":
        raise SystemExit(f"Unexpected PNG mode {im.mode}")
    print(f"PNG {im.size[0]}x{im.size[1]} mode={im.mode} opaque=yes")


def main() -> int:
    for label, fg, bg in (
        ("wordmark on plate", FG, BG),
        ("mint badge on plate", MINT, BG),
        ("check on mint badge", BG, MINT),
    ):
        ratio = contrast_ratio(fg, bg)
        print(f"contrast {label}: {ratio:.2f}:1")
        if ratio < 4.5:
            raise SystemExit(f"Contrast below 4.5:1 for {label}")

    ASSETS.mkdir(exist_ok=True)
    svg_path = ASSETS / "logo.svg"
    png_path = ASSETS / "logo.png"
    svg_path.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {svg_path}")
    render_png(svg_path, png_path)
    assert_png(png_path)
    print(f"wrote {png_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
