import matplotlib.pyplot as plt


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
