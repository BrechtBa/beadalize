import numpy as np
import matplotlib.pyplot as plt


from beadalize.shared import SvgConvertable


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


class HexagonPlatformTilted(HexagonPlatform):
    def coordinates(self):
        coordinates = super().coordinates()
        return [[c[1], c[0]] for c in coordinates]


class SquarePlatform(Platform):
    def __init__(self, *args, size=16, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = size

    def coordinates(self):
        x = []
        y = []
        for i in range(self.size):
            for j in range(self.size):
                y.append(i*self.module)
                x.append(j*self.module)
        return list(zip(x, y))


class RectangularPlatform(Platform):
    def __init__(self, *args, width=24, height=16, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height

    def coordinates(self):
        x = []
        y = []
        for i in range(self.height):
            for j in range(self.width):
                y.append(i*self.module)
                x.append(j*self.module)
        return list(zip(x, y))


def get_platform(class_name, *args, **kwargs):
    classes = {
        'HexagonPlatform': HexagonPlatform,
        'HexagonPlatformTilted': HexagonPlatformTilted,
        'RectangularPlatform': RectangularPlatform
    }
    return classes.get(class_name)(*args, **kwargs)
