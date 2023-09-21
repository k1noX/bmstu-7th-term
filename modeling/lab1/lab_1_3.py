"""
    5.14
    Найти минимум функции 2-х переменных f (x, y)
    с точностью 1e-6
    на прямоугольнике [x_1, x_2] x [y_1, y_2]
     ПОРЯДОК РЕШЕНИЯ ЗАДАЧИ:
    1. Задать указанную в варианте функцию
    f (x, y).
    2. Построить графики функции и поверхностей уровня
    f (x, y).
    3. По графикам найти точки начального приближения к точкам экстремума.
    4. Найти экстремумы функции c заданной точностью.
    3 * x^2 +  2 * y^4+y*cos(e^2x)
    x_1=-1, x_2=1
    t_1=-1, t_2=1
"""
import logging
import typing as _t

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize


def _function(x: float, y: float) -> float:
    return 3 * np.power(x, 2) + 2 * np.power(y, 4) + y * np.cos(np.exp(2 * x))


def get_function_minimum(
        function: _t.Callable[[float, float], float],
        initial_guess: _t.List[float]
) -> (float, float):
    _initial_guess = np.array(initial_guess)
    result = optimize.minimize(lambda args: function(*args), _initial_guess)
    if result.success:
        fitted_params = result.x
        return tuple(fitted_params)
    else:
        raise ValueError(result.message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _log = logging.getLogger()
    _log.setLevel(logging.INFO)

    x_0 = -1
    x_1 = 1
    y_0 = -1
    y_1 = 1
    points = 100

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    x, y = np.meshgrid(
        np.linspace(x_0, x_1, points),
        np.linspace(y_0, y_1, points)
    )
    z = _function(x, y)
    ax.plot_surface(x, y, z)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('f(x,y)')
    plt.show()

    fig, ax = plt.subplots(1, 1)
    ax.contour(x, y, z, levels=13)
    fig.set_figwidth(8)
    fig.set_figheight(8)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('f(x,y)')
    plt.show()

    _initial_guess = [-1.0, 1.0]
    min_x, min_y = get_function_minimum(_function, _initial_guess)
    _log.info("Точка минимума: (%.6f; %.6f)", min_x, min_y)
    _log.info("f(%.6f, %.6f)=%.6f", min_x, min_y, _function(min_x, min_y))
