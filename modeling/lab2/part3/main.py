# Вариант 14
from functools import reduce
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines
from matplotlib.animation import FuncAnimation


class Animation:
    def __init__(
            self, xs, ys, line, points, min_label,
            root_label, conditions
    ):
        self._xs = xs
        self._ys = ys
        self._line = line
        self._points = points
        self._min_label = min_label
        self._root_label = root_label
        self._previous_points = []
        self._pause = False
        self._previous_root = 20
        self._conditions = conditions

    def to_tuple(self) -> tuple:
        return (
            self._line,
            self._points,
            self._min_label,
            self._root_label,
        )

    def get_frames(self):
        MAX_ROOT = 50
        STEP = 0.05
        while self._previous_root < MAX_ROOT:
            if not self._pause:
                self._previous_root += STEP
            yield self._previous_root

    def on_click(self, event):
        self._pause ^= True

    def get_animation_frame(self, z: float) -> tuple:
        y = (z - 4 * self._xs) / 6
        self._line.set_data(self._xs, y)

        regions = [condition(self._xs, y) for condition in conditions]
        intersection = list(reduce(lambda _x, _y: _x & _y, regions))

        points = {}
        for i in range(len(self._xs)):
            for j in range(len(y)):
                if intersection[i][j]:
                    points[self._xs[i][j]] = y[i][j]

        if len(points.keys()) > 0 and len(self._previous_points) > 0:
            x_min = list(points.keys())[0]
            y_min = list(points.values())[0]
            min_label.set_text(
                f"min $z$ = $f({x_min:.2f}, {y_min:.2f})$ ="
                f" {z:.2f}"
            )
            self._pause = True

        points_tuple = ([*points.keys()], [*points.values()])
        self._previous_points = points_tuple
        self._points.set_data(*points_tuple)

        return self.to_tuple()


if __name__ == "__main__":
    conditions = [
        lambda x, y: 3 * x + y >= 9,
        lambda x, y: x + 2 * y >= 8,
        lambda x, y: x + 6 * y >= 11
    ]

    equalities = [
        lambda x, y: 3 * x + y - 9,
        lambda x, y: x + 2 * y - 8,
        lambda x, y: x + 6 * y - 11
    ]
    colors = [
        "#ffa700B0",
        "#0057e7B0",
        "#008744B0"
    ]

    values = np.linspace(0, 7, 250)
    xs, ys = np.meshgrid(values, values)

    regions = [condition(xs, ys) for condition in conditions]
    extent = (xs.min(), xs.max(), ys.min(), ys.max())

    figure, axis = plt.subplots()

    for i in range(len(equalities)):
        plt.contour(xs, ys, equalities[i](xs, ys), [0], colors=colors[i])

    intersetion = np.array(reduce(lambda _x, _y: _x & _y, regions))
    plt.imshow(
        intersetion.astype(int),
        extent = extent,
        origin = "lower",
        cmap = "Reds",
        alpha = 0.5
    )

    line = axis.plot([], [], "r")[0]
    points = axis.plot([], [], "ro")[0]
    min_label = axis.text(0.1, 0.3, "", fontsize=10)
    max_label = axis.text(0.1, 0.1, "", fontsize=10)
    root_label = axis.text(0.1, 0.5, "", fontsize=10)

    animation = Animation(
        xs, ys, line, points, min_label, root_label, conditions
    )
    ani = FuncAnimation(
        figure,
        animation.get_animation_frame,
        frames = animation.get_frames,
        init_func = animation.to_tuple,
        blit = True,
        interval = 10,
    )
    figure.canvas.mpl_connect('button_press_event', animation.on_click)

    green_legend_handle = matplotlib.lines.Line2D(
        [], [], color=colors[0], marker="s", ls="",
        label="$x_1$ + $x_2$ <= 6"
    )
    blue_legend_handle = matplotlib.lines.Line2D(
        [], [], color=colors[1], marker="s", ls="",
        label="($x_1$ - 2)($x_2$ + 1) >= 4"
    )
    blue_legend_handle = matplotlib.lines.Line2D(
        [], [], color=colors[2], marker="s", ls="",
        label="($x_1$ - 2)($x_2$ + 1) >= 4"
    )

    plt.legend(handles=[green_legend_handle, blue_legend_handle])

    plt.show()
