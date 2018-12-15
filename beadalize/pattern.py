import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from scipy import ndimage

from beadalize.shared import SvgConvertable
from beadalize.bead import Bead


class Pattern(SvgConvertable):
    def __init__(self, platform, palette=None, bead_type=Bead,
                 image_path=None, scale=1.0, xoffset=0.0, yoffset=0.0, rotation=0):
        self.platform = platform
        self.palette = palette
        self.beads = [bead_type(module=self.platform.module) for _ in range(len(self.platform.coordinates()))]

        self.image_path = image_path
        self.scale = scale
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.rotation = rotation

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        self.platform.plot(ax=ax)

        patches = []
        for b, c in zip(self.beads, self.platform.coordinates()):
            p = b.plot(ax=ax, x=c[0], y=c[1])
            patches.append(p)
        return patches

    @property
    def image(self):
        img = image.imread(self.image_path)
        img = ndimage.rotate(img, self.rotation)
        if img.shape[2] == 4:
            # flatten alpha
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    a = img[i, j, 3]
                    img[i, j, 0] = 1 * (1 - a) + img[i, j, 0] * a
                    img[i, j, 1] = 1 * (1 - a) + img[i, j, 1] * a
                    img[i, j, 2] = 1 * (1 - a) + img[i, j, 2] * a
        img = img[:, :, :3]

        return img

    @property
    def image_bounds(self):
        img = self.image
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

        img_xmin = xmin + self.xoffset
        img_xmax = xmin + self.xoffset + img_dx*self.scale
        img_ymin = ymin + self.yoffset
        img_ymax = ymin + self.yoffset + img_dy*self.scale
        return img_xmin, img_xmax, img_ymin, img_ymax

    def plot_image(self, ax=None):
        img_xmin, img_xmax, img_ymin, img_ymax = self.image_bounds

        if ax is None:
            ax = plt.gca()

        self.plot(ax=ax)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        pl = ax.imshow(self.image, extent=[img_xmin, img_xmax, img_ymin, img_ymax])
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        return pl

    def get_colors(self):
        img = self.image
        img_xmin, img_xmax, img_ymin, img_ymax = self.image_bounds

        coordinates = self.platform.coordinates()

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
