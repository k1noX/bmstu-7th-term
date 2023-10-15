# Вариант 14
from functools import reduce

import matplotlib.lines
import matplotlib.pyplot as plt
import numpy as np

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

    explicit_equalities = [
        lambda x: 9 - 3 * x,
        lambda x: 4 - x / 2,
        lambda x: (11 - x) / 6,
    ]

    labels = [
        '$3x_1 + x_2 = 9$',
        '$x_1 + 2x_2 = 8$',
        '$x_1 + 6x_2 = 11$'
    ]

    colors = [
        "k-.",
        "k--",
        "k:"
    ]

    figure, axis = plt.subplots()

    x = np.arange(0, 12, 0.01)

    plan = (26 - 4 * x) / 6
    plt.plot(x, plan, "r--", label=f'$z = 4x_1 + 6x_2 = 26$')
    plan = (30.8 - 4 * x) / 6
    plt.plot(x, plan, "r-.", label=f'$z = 4x_1 + 6x_2 = 30.8$')
    plan = (44 - 4 * x) / 6
    plt.plot(x, plan, "r-.", label=f'$z = 4x_1 + 6x_2 = 44$')

    point_name = ord('A')
    for i in range(len(explicit_equalities)):
        previous_i = i - 1 if i != 0 else len(explicit_equalities) - 1
        previous_f = explicit_equalities[previous_i](x)
        f = explicit_equalities[i](x)
        idx = np.argwhere(np.diff(np.sign(previous_f - f))).flatten()[0]
        plt.plot(x, f, colors[i], label=labels[i])
        plt.plot(x[idx], f[idx], 'ko')
        axis.annotate(
            f'{chr(point_name)} ({x[idx]:.1f}, {f[idx]:.1f})',
            (x[idx] - 0.5, f[idx] + 0.3),
            backgroundcolor='#ffffffB0'
        )
        point_name += 1

    for i in range(len(explicit_equalities)):
        if i != 2:
            continue
        f = explicit_equalities[i](x)
        idx = np.argwhere(np.diff(np.sign(f))).flatten()[0]
        plt.plot(x[idx], f[idx], 'ko')
        axis.annotate(
            f'{chr(point_name)} ({x[idx]:.1f}, {f[idx]:.1f})',
            (x[idx] - 0.5, f[idx] + 0.3),
            backgroundcolor='#ffffffB0'
        )
        point_name += 1

    plt.axvline(2, color='b', linestyle='--', label='$x_1=2$')
    plt.axvline(6.5, color='b', linestyle='-.', label='$x_1=6.5$')
    plt.axvline(11, color='b', linestyle=':', label='$x_1=11$')
    axis.set_ylim(0, 7)
    axis.set_xlim(0, 12)

    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")

    xs, ys = np.meshgrid(x, x)
    regions = [condition(xs, ys) for condition in conditions]
    intersection = np.array(reduce(lambda _x, _y: _x & _y, regions))
    extent = (x.min(), x.max(), x.min(), x.max())
    plt.imshow(
        intersection.astype(int),
        extent=extent,
        origin="lower",
        cmap="Greens",
        alpha=0.25
    )

    plt.legend()
    plt.show()
