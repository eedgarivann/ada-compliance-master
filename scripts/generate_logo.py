#!/usr/bin/env python3
"""Rebuild assets/logo.svg from the measured geometry of the author logo.

The committed assets/logo.png is a 1024x1024 LANCZOS resize of the author's
original raster (1408x1408, opaque RGB). This script only rewrites the SVG
companion so it stays in lockstep with those measurements. It does not
invent a new mark.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# Sampled from solid pixels of the author's PNG.
NAVY = "#2A3785"
WHITE = "#FFFFFF"

# Source canvas is 1408x1408. Outer circle is centered; radius 628 leaves a
# 76px white margin. Inner circle from a least-squares fit of the hole edge.
VIEWBOX = 1408
OUTER_CX, OUTER_CY, OUTER_R = 704, 704, 628
INNER_CX, INNER_CY, INNER_R = 475.368, 485.959, 118.771


def build_svg() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 {VIEWBOX} {VIEWBOX}" role="img" aria-labelledby="logo-title logo-desc">
  <title id="logo-title">ADA Compliance Master</title>
  <desc id="logo-desc">A navy circle with a smaller white circle in the upper left, on a solid white square.</desc>
  <rect width="{VIEWBOX}" height="{VIEWBOX}" fill="{WHITE}"/>
  <circle cx="{OUTER_CX}" cy="{OUTER_CY}" r="{OUTER_R}" fill="{NAVY}"/>
  <circle cx="{INNER_CX}" cy="{INNER_CY}" r="{INNER_R}" fill="{WHITE}"/>
</svg>
'''


def main() -> int:
    ASSETS.mkdir(exist_ok=True)
    path = ASSETS / "logo.svg"
    path.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
