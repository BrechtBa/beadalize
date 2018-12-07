import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image

from beadalize.shared import SvgConvertable
from beadalize.bead import Bead


class Pattern(SvgConvertable):
    def __init__(self, platform, palette=None, bead_type=Bead):
        self.platform = platform
        self.palette = palette
        self.beads = [bead_type(module=self.platform.module) for _ in range(len(self.platform.coordinates()))]

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        self.platform.plot(ax=ax)

        patches = []
        for b, c in zip(self.beads, self.platform.coordinates()):
            p = b.plot(ax=ax, x=c[0], y=c[1])
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

        pixel_y = np.interp(range(img.shape[0]), [-0.5, img.shape[0] - 0.5], [img_ymax, img_ymin])
        pixel_x = np.interp(range(img.shape[1]), [-0.5, img.shape[1] - 0.5], [img_xmin, img_xmax])

        for b, c in zip(self.beads, coordinates):
            j_center = int(np.round(np.interp(c[0], [img_xmin, img_xmax], [-0.5, img.shape[1]-0.5])))
            i_center = int(np.round(np.interp(c[1], [img_ymin, img_ymax], [img.shape[0]-0.5, -0.5])))
            dj = 2
            di = 2

            original_colors = []
            for j in range(max(0, j_center-dj), min(img.shape[1], j_center+dj)):
                for i in range(max(0, i_center-di), min(img.shape[0], i_center+di)):
                    if b.is_inside(pixel_x[j] - c[0], pixel_y[i] - c[1]):
                        original_colors.append(img[i, j, :])

            if len(original_colors) > 0:
                original_color = np.mean(np.array(original_colors), axis=0)
                if self.palette is not None:
                    b.color = self.palette.nearest(tuple(np.round(original_color, 4)))
                else:
                    b.color = original_color

        # plotting for testing
        # fig, ax = plt.subplots()
        # self.plot(ax=ax)
        # xlim = ax.get_xlim()
        # ylim = ax.get_ylim()
        # pl = ax.imshow(img, extent=[img_xmin, img_xmax, img_ymin, img_ymax])
        # ax.set_xlim(xlim)
        # ax.set_ylim(ylim)
