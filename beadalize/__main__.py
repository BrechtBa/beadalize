import argparse
import json

import matplotlib.pyplot as plt

from beadalize.palette import hama_color_palette
from beadalize.platform import get_platform
from beadalize.pattern import Pattern


parser = argparse.ArgumentParser(description='.')
parser.add_argument('--input', type=str, default=None,
                    help='path to a png image to convert to a bead pattern')
parser.add_argument('--output', type=str, default=None,
                    help='path to write the svg output to')
parser.add_argument('--scale', type=float, default=1.0,
                    help='scale')
parser.add_argument('--xoffset', type=float, default=0.0,
                    help='xoffset')
parser.add_argument('--yoffset', type=float, default=0.0,
                    help='yoffset')
parser.add_argument('--rotation', type=float, default=0.0,
                    help='rotation')
parser.add_argument('--platform', type=str, default='HexagonPlatform',
                    help='platform')
parser.add_argument('--platform-kwargs', type=json.loads, default={},
                    help='platform keyword arguments')
parser.add_argument('--palette', type=str, default='hama_color_palette',
                    help='palette')
parser.add_argument('--no-pattern', dest='no_pattern', action='store_const',
                    const=True, default=False,
                    help='skip pattern generation')
args = parser.parse_args()

palette = hama_color_palette
platform = get_platform(args.platform, **args.platform_kwargs)
pattern = Pattern(platform, palette=palette, image_path=args.input,
                  scale=args.scale, xoffset=args.xoffset, yoffset=args.yoffset, rotation=args.rotation)

if args.no_pattern:
    fig, ax = plt.subplots()
    pattern.plot_image(ax=ax)
else:
    pattern.get_colors()
    fig, ax = plt.subplots()
    pattern.plot(ax=ax)

if args.output is not None:
    pattern.to_svg(args.output)

plt.show()
