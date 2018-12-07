import matplotlib.pyplot as plt

from beadalize.palette import hama_color_palette
from beadalize.platform import HexagonPlatform
from beadalize.pattern import Pattern

fig, ax = plt.subplots()
hama_color_palette.plot(ax=ax)

platform = HexagonPlatform(module=5, size=32)
pattern = Pattern(platform, palette=hama_color_palette)
pattern.colors_from_bitmap('examples/mountain.png', scale=1.4, xoffset=0, yoffset=0)
pattern.to_svg('examples/mountain.svg')

fig, ax = plt.subplots()
pattern.plot(ax=ax)
plt.show()
