import matplotlib.pyplot as plt

from beadalize.palette import hama_color_palette
from beadalize.platform import HexagonPlatform
from beadalize.pattern import Pattern

fig, ax = plt.subplots()
hama_color_palette.plot(ax=ax)

palette = hama_color_palette.subset([0, 2, 4, 28, 35, 54])

fig, ax = plt.subplots()
palette.plot(ax=ax)

platform = HexagonPlatform(module=5, size=16)
pattern = Pattern(platform, palette=palette,
                  image_path='rocket.png', scale=0.80, xoffset=20, yoffset=9, rotation=14)
fig, ax = plt.subplots()
pattern.plot_image(ax=ax)

pattern.get_colors()
pattern.to_svg('rocket.svg')

fig, ax = plt.subplots()
pattern.plot(ax=ax)
plt.show()
