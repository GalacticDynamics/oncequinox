# /// script
# requires-python = ">=3.11"
# dependencies = ["resvg-py"]
# ///
"""Draw the oncequinox logo: Equinox's, with a 1 cut into it.

Equinox's logo is a circle, solid on the left and a checkerboard on the right.
oncequinox's cuts a big 1 out of the solid half: an Equinox module, made once.
The 1 is cut out with an SVG mask, so it shows whatever the logo sits on. The
shapes are vector, so the logo is written as an SVG, sharp at any size; for a
bitmap, name a .png and give its size::

    uv run docs/_static/make_logo.py                     # favicon.svg
    uv run docs/_static/make_logo.py --size 2048 big.png
"""

import argparse
from pathlib import Path

# Equinox's logo: Material Design Icons' "circle-opacity", by Pictogrammers,
# under the Apache License 2.0 (https://pictogrammers.com/library/mdi/).
CIRCLE = (
    "M18 10V8H20V10H18M18 12V10H16V12H18M18 8V6H16V8H18M16 2.84V4H18"
    "C17.37 3.54 16.71 3.15 16 2.84M18 4V6H20C19.42 5.25 18.75 4.58 18 4"
    "M20 6V8H21.16C20.85 7.29 20.46 6.63 20 6M22 12"
    "C22 11.32 21.93 10.65 21.8 10H20V12H22M16 6V4H14V6H16M16 16H18V14H16"
    "V16M18 18H20L20 18V16H18V18M16 20H18L18 20V18H16V20M14 21.8"
    "C14.7 21.66 15.36 21.44 16 21.16V20H14V21.8M18 14H20V12H18V14M16 8H14"
    "V10H16V8M20 16H21.16C21.44 15.36 21.66 14.7 21.8 14H20V16M16 12H14V14"
    "H16V12M12 18V16H14V14H12V12H14V10H12V8H14V6H12V4H14V2.2"
    "C13.35 2.07 12.69 2 12 2C6.5 2 2 6.5 2 12S6.5 22 12 22V20H14V18H12"
    "M14 18H16V16H14V18Z"
)
NAVY = "#030a23"  # GalacticDynamics' navy
# The 1, in the icon's 24-unit grid: its flag, stem and foot, and their width.
ONE = "M7.3 9.2L9.4 7.4V16.6M7.3 16.6H11.3"
ONE_WIDTH = 1.7

SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="512" height="512">
  <mask id="cut">
    <rect width="24" height="24" fill="#fff"/>
    <path d="{one}" stroke="#000" stroke-width="{width:g}" fill="none"
      stroke-linecap="round" stroke-linejoin="round"/>
  </mask>
  <path d="{circle}" fill="{navy}" mask="url(#cut)"/>
</svg>
"""


def svg() -> str:
    """Return the logo as SVG text."""
    return SVG.format(circle=CIRCLE, one=ONE, width=ONE_WIDTH, navy=NAVY)


def main() -> None:
    """Parse the command line and save the logo."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "out",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("favicon.svg"),
        help="output file, SVG or PNG by its extension (default: favicon.svg)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=512,
        help="pixels per side, for a PNG",
    )
    args = parser.parse_args()

    if args.out.suffix == ".svg":
        args.out.write_text(svg())
    else:
        import resvg_py  # noqa: PLC0415  # only a PNG needs a renderer

        png = resvg_py.svg_to_bytes(svg_string=svg(), width=args.size)
        args.out.write_bytes(bytes(png))


if __name__ == "__main__":
    main()
