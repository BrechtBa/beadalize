import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Bead:
    def __init__(self, module=5, color=None):
        self.module = module
        self.color = color

    def is_inside(self, x, y):
        return x**2 + y**2 <= (0.5*self.module)**2

    def plot(self, ax=None, x=None, y=None):
        if ax is None:
            ax = plt.gca()
        p = patches.Circle((x, y), 0.5 * self.module, facecolor=self.color if self.color is not None else 'None',
                           edgecolor=(0.2, 0.2, 0.2), linewidth=0.5)
        ax.add_patch(p)
        return p


class SquareBead(Bead):
    def is_inside(self, x, y):
        return (-0.5*self.module <= x) and (x <= 0.5*self.module) and (-0.5*self.module <= y) and (y <= 0.5*self.module)

    def plot(self, ax=None, x=None, y=None):
        if ax is None:
            ax = plt.gca()
        p = patches.Rectangle((x-0.5*self.module, y-0.5*self.module), 0.5 * self.module, 0.5 * self.module,
                              facecolor=self.color if self.color is not None else 'None', edgecolor=(0.2, 0.2, 0.2),
                              linewidth=0.5)
        ax.add_patch(p)
        return p
