import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure


def function(x_1: float, x_2: float, x_3: float, z: float) -> float:
    return 2 * x_1 - x_2 + x_3 - z


def condition(x_1: float, x_2: float, x_3: float) -> float:
    return np.power(x_1, 2) + np.power(x_2, 2) + np.power(x_3, 2) - 1


def plot_implicit(
        axis: plt.Axes, fn, bbox=(-2.5, 2.5), color="red",
        order=1
):
    xl = np.linspace(-3, 3, 25)
    X, Y, Z = np.meshgrid(xl, xl, xl)
    F = fn(X, Y, Z)
    verts, faces, normals, values = measure.marching_cubes(
        F, 0, spacing=[np.diff(xl)[0]] * 3
    )
    verts -= 3
    axis.plot_trisurf(
        verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces,
        color=color, lw=0, zorder=order
    )


def plot_implicit_contour(
        axis: plt.Axes, fn, bbox=(-2.5, 2.5), color="red",
        order=1
):
    A = np.linspace(-1, 1, 100)  # resolution of the contour
    B = np.linspace(-1, 1, 15)  # number of slices
    A1, A2 = np.meshgrid(A, A)  # grid on which the contour is plotted

    for z in B:  # plot contours in the XY plane
        X, Y = A1, A2
        Z = fn(X, Y, z)
        cset = axis.contour(
            X, Y, Z + z, [z], zdir="z", colors=[color],
            zorder=order
        )
        # [z] defines the only level to plot for this contour for this value of z

    for y in B:  # plot contours in the XZ plane
        X, Z = A1, A2
        Y = fn(X, y, Z)
        cset = axis.contour(
            X, Y + y, Z, [y], zdir="y", colors=[color],
            zorder=order
        )

    for x in B:  # plot contours in the YZ plane
        Y, Z = A1, A2
        X = fn(x, Y, Z)
        cset = axis.contour(
            X + x, Y, Z, [x], zdir="x", colors=[color],
            zorder=order
        )


def show_result_plot(
        function,
        condition,
        z: float,
        point: list,
        colors: dict,
        legend: list
):
    figure = plt.figure()
    axis = figure.add_subplot(111, projection="3d", computed_zorder=False)
    plot_implicit(axis, condition, color=colors["red"], order=1)
    plot_implicit_contour(
        axis, lambda x_1, x_2, x_3: function(x_1, x_2, x_3, z),
        color=colors["blue"], order=2
    )
    axis.plot(
        point[0], point[1], point[2], ".", c=colors["black"],
        markersize=20, zorder=3
    )
    axis.set_xlabel("$x_1$")
    axis.set_ylabel("$x_2$")
    axis.set_zlabel("$x_3$")
    axis.set_xlim(-1, 1)
    axis.set_ylim(-1, 1)
    axis.set_zlim(-1, 1)

    plt.legend(
        handles=legend
    )
    plt.show()


if __name__ == "__main__":
    colors = {
        "red": "#B34B3E",
        "blue": "#0174C3",
        "black": "#5DCA6E"
    }

    min_z = -6 * np.sqrt(1 / 6)
    red_legend_handle = matplotlib.lines.Line2D(
        [], [], color=colors["red"], marker="s", ls="",
        label="$x_1^2$ + $x_2^2$ + $x_3^2$ = 1"
    )
    blue_legend_handle = matplotlib.lines.Line2D(
        [], [], color=colors["blue"], marker="s", ls="",
        label=f"2$x_1$ - $x_2$ + $x_3$ = {min_z:.4f}"
    )
    green_legend_handle = matplotlib.lines.Line2D(
        [], [], color=colors["black"], marker="s", ls="",
        label=f"M = ({-np.sqrt(2 / 3):.2f}, "
              f"{np.sqrt(2 / 12):.2f}, {-np.sqrt(2 / 12):.2f})"
    )
    legend = [red_legend_handle, blue_legend_handle, green_legend_handle]
    point = [-np.sqrt(2 / 3), np.sqrt(2 / 12), -np.sqrt(2 / 12)]
    show_result_plot(function, condition, min_z, point, colors, legend)

    max_z = 6 * np.sqrt(1 / 6)
    blue_legend_handle = matplotlib.lines.Line2D(
        [], [], color="blue", marker="s", ls="",
        label=f"2$x_1$ - $x_2$ + $x_3$ = {max_z:.4f}"
    )
    green_legend_handle = matplotlib.lines.Line2D(
        [], [], color="green", marker="s", ls="",
        label=f"M = ({np.sqrt(2 / 3):.2f}, "
              f"{-np.sqrt(2 / 12):.2f}, {np.sqrt(2 / 12):.2f})"
    )
    legend = [red_legend_handle, blue_legend_handle, green_legend_handle]
    point = [np.sqrt(2 / 3), -np.sqrt(2 / 12), np.sqrt(2 / 12)]
    show_result_plot(function, condition, max_z, point, colors, legend)
