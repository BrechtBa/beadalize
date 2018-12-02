import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.patches import Circle


class SvgConvertable:
    def plot(self, ax=None):
        return None

    def to_svg(self, path):
        fig, ax = plt.subplots()
        self.plot(ax=ax)
        ax.set_axis_off()
        ax.set_position([0, 0, 1, 1])

        xlim = ax.get_xlim()
        dx = xlim[1] - xlim[0]
        ylim = ax.get_ylim()
        dy = ylim[1] - ylim[0]
        fig.set_size_inches(dx/25.4, dy/25.4)

        fig.savefig(path, dpi=100, format='svg')
        plt.close(fig)


class Platform(SvgConvertable):
    def __init__(self, module=5):
        self.module = module

    def __len__(self):
        pass

    def coordinates(self):
        pass

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        c = self.coordinates()
        p = ax.plot(*zip(*c), 'k.', markersize=1)
        ax.set_aspect('equal')
        return p


class HexagonPlatform(Platform):
    def __init__(self, *args, size=16, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = size

    def coordinates(self):
        x = []
        y = []
        d = np.sin(60*np.pi/180)
        for i in range(self.size):
            for j in range(self.size + i):
                y.append(i*self.module * d)
                x.append(j*self.module - 0.5 * i * self.module)

        for i in range(self.size-1):
            for j in range(2*self.size - i - 2):
                y.append((self.size + i) * self.module * d)
                x.append(j * self.module - 0.5 * (self.size - i - 2) * self.module)
        return list(zip(x, y))


class Bead:
    def __init__(self, module=5, color=None):
        self.module = module
        self.color = color


class Palette:
    def __init__(self, colors):
        self.colors = colors

    @staticmethod
    def distance(color1, color2):
        from colormath.color_objects import sRGBColor, LabColor
        from colormath.color_conversions import convert_color
        from colormath.color_diff import delta_e_cie2000

        color1_rgb = sRGBColor(*color1)
        color2_rgb = sRGBColor(*color2)

        color1_lab = convert_color(color1_rgb, LabColor)
        color2_lab = convert_color(color2_rgb, LabColor)

        return delta_e_cie2000(color1_lab, color2_lab)

    def nearest(self, color):
        dists = [self.distance(color, c) for c in self.colors]
        val, index = min((val, idx) for (idx, val) in enumerate(dists))
        return self.colors[index]


class Pattern(SvgConvertable):
    def __init__(self, platform, palette):
        self.platform = platform
        self.palette = palette
        self.beads = [Bead(module=self.platform.module) for _ in range(len(self.platform.coordinates()))]

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        self.platform.plot(ax=ax)

        patches = []
        for b, c in zip(self.beads, self.platform.coordinates()):
            p = Circle(c, 0.5*b.module, facecolor=b.color if b.color is not None else 'None', edgecolor=(0.3, 0.3, 0.3),
                       linewidth=1, alpha=1.0)
            ax.add_patch(p)
            patches.append(p)
        return patches

    def colors_from_bitmap(self, path, scale=1.0, xoffset=0.0, yoffset=0.0):
        img = image.imread(path)

        if img.shape[2] == 4:
            # flatten alpha
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    a = img[i, j, 3]
                    img[i, j, 0] = 1 * (1 - a) + img[i, j, 0] * a
                    img[i, j, 1] = 1 * (1 - a) + img[i, j, 1] * a
                    img[i, j, 2] = 1 * (1 - a) + img[i, j, 2] * a
        img = img[:, :, :3]

        coordinates = self.platform.coordinates()
        x, y = zip(*coordinates)
        xmin = min(x) - 0.5*self.platform.module
        xmax = max(x) + 0.5*self.platform.module
        dx = xmax - xmin
        ymin = min(y) - 0.5 * self.platform.module
        ymax = max(y) + 0.5 * self.platform.module
        dy = ymax - ymin
        img_dx = img.shape[1] * min(dx/img.shape[1], dy/img.shape[0])
        img_dy = img.shape[0] * min(dx/img.shape[1], dy/img.shape[0])

        img_xmin = xmin + xoffset
        img_xmax = xmin + xoffset + img_dx*scale
        img_ymin = ymin + yoffset
        img_ymax = ymin + yoffset + img_dy*scale

        for b, c in zip(self.beads, coordinates):
            j = int(np.round(np.interp(c[0], [img_xmin, img_xmax], [-0.5, img.shape[1]-0.5])))
            i = int(np.round(np.interp(c[1], [img_ymin, img_ymax], [img.shape[0]-0.5, -0.5, ])))
            if 0 <= i < img.shape[0] and 0 <= j < img.shape[1]:
                original_color = img[i, j, :]
                b.color = self.palette.nearest(original_color)

        # plotting for testing
        fig, ax = plt.subplots()
        self.plot(ax=ax)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        pl = ax.imshow(img, extent=[img_xmin, img_xmax, img_ymin, img_ymax])
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)


default_color_palette = Palette([
    (116/255,  33/255,  38/255),
    (207/255,  70/255, 142/255),
    (167/255,  85/255, 151/255),
    ( 27/255,  61/255, 116/255),
    ( 52/255,  27/255,  30/255),
    ( 23/255,  25/255,  28/255),
    ( 55/255, 118/255, 144/255),
    (141/255, 140/255, 136/255),
    (114/255,  81/255, 144/255),
    (210/255,  84/255,  72/255),
    (137/255,  21/255,  36/255),
    (168/255,  65/255,  66/255),
    (169/255, 114/255,  44/255),
    ( 37/255,  32/255,  76/255),
    (140/255, 139/255, 146/255),
    (161/255, 137/255,  87/255),
    (236/255, 236/255, 236/255),
    (189/255, 116/255, 145/255),
    (  0/255,  65/255,  36/255),
    (  0/255,  53/255,  29/255),
])

if __name__ == '__main__':
    platform = HexagonPlatform(module=5, size=16)
    pattern = Pattern(platform, default_color_palette)

    pattern.colors_from_bitmap('/home/brecht/Pictures/kerstboom.png', scale=1.1, xoffset=5, yoffset=-10)
    pattern.to_svg('/tmp/test.svg')
    plt.show()
