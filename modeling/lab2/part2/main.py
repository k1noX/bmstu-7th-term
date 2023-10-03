import matplotlib.pyplot as plt
import numpy as np
from skimage import measure


def function(x_1: float, x_2: float, x_3: float, z: float) -> float:
    return 2 * x_1 - x_2 + x_3 - z


def condition(x_1: float, x_2: float, x_3: float) -> float:
    return np.power(x_1, 2) + np.power(x_2, 2) + np.power(x_3, 2) - 1


def plot_implicit(axis: plt.Axes, fn, bbox=(-2.5, 2.5), color="red"):
    xl = np.linspace(-3, 3, 25)
    X, Y, Z = np.meshgrid(xl, xl, xl)
    F = fn(X, Y, Z)
    verts, faces, normals, values = measure.marching_cubes(
        F, 0, spacing=[np.diff(xl)[0]] * 3
    )
    verts -= 3
    axis.plot_trisurf(
        verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces,
        color=color, lw=0
    )
    axis.set_xlim(-1, 1)
    axis.set_ylim(-1, 1)
    axis.set_zlim(-1, 1)


if __name__ == "__main__":
    figure = plt.figure()
    axis = figure.add_subplot(111, projection='3d')
    plot_implicit(axis, condition, color="blue")
    plot_implicit(
        axis, lambda x_1, x_2, x_3: function(
            x_1, x_2, x_3,
            -6 * np.sqrt(1 / 6)
        )
    )
    plt.show()
