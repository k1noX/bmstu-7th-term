"""
Задача 6. Указанным в индивидуальном варианте методом найти минимум
квадратичной функции
с точностью 1e-6. Для решения задачи многомерной минимизации использовать метод
Ньютона. Построить график функции f. Предусмотреть подсчет числа
итераций, потребовавшихся для достижения заданной точности.
a_11=4
2a_12=-0.5
a_22=0.5
2a_13=-2.2
2a_23=-1.8
Наискорейший спуск
https://sophiamyang.github.io/DS/optimization/descentmethod2/descentmethod2.html
"""
import logging
import sys
import typing as _t

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


def _function(x: float, y: float) -> float:
    return (4 * np.power(x, 2) - 0.5 * x * y + 0.5 * np.power(y, 2) - 2.2 *
            x - 1.8 * y)


def dfdx(x: float, y: float) -> float:
    return 8 * x - 0.5 * y - 2.2


def df2dx2(x: float, y: float) -> float:
    return 8


def dfdy(x: float, y: float) -> float:
    return - 0.5 * x + y - 1.8


def df2dy2(x: float, y: float) -> float:
    return 1


def _newton_method(
        x: float, y: float, tolerance: float,
        variable: str
) -> _t.Tuple[float, float]:
    iteration = 0
    if variable == 'x':
        while True:
            x1 = x - dfdx(x, y) / df2dx2(x, y)
            dx = abs(x1 - x)
            x = x1
            iteration += 1
            if dx < tolerance:
                break
    if variable == 'y':
        while True:
            y1 = y - dfdy(x, y) / df2dy2(x, y)
            dy = abs(y1 - y)
            y = y1
            iteration += 1
            if dy < tolerance:
                break
    return [x, y], iteration


def steepest_descend_method(
        function: _t.Callable[[_t.List[float]], float],
        x0: _t.List[float], tolerance: float = 1e-6
) -> _t.Tuple[_t.List, float]:
    x = np.array(x0)

    def gradient(
            function: _t.Callable[[_t.List[float]], float],
            current: _t.List[float],
            tolerance: float
    ) -> np.array:
        return optimize.approx_fprime(current, function, tolerance ** 2)

    grad = gradient(function, x, tolerance)
    iteration = 0

    while any([abs(grad[i]) > tolerance for i in range(len(grad))]):
        grad = gradient(function, x, tolerance)
        a = optimize.minimize_scalar(lambda k: function(*[x + k * grad])).x
        x += a * grad
        iteration += 1

    return list(x), iteration


def newton_method(
        function: _t.Callable[[float, float], float],
        x0: _t.List[float], tolerance: float = 1e-6
) -> _t.Tuple[_t.List, float]:
    x = x0[0]
    y = x0[1]
    difference = sys.float_info.max
    iteration = 0
    while difference > tolerance:
        [x, y], sub_iters = _newton_method(x, y, tolerance, 'x')
        f1 = function(x, y)
        iteration += sub_iters
        [x, y], sub_iters = _newton_method(x, y, tolerance, 'y')
        f2 = function(x, y)
        iteration += sub_iters
        difference = abs(f1 - f2)
    return [x, y], iteration


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _log = logging.getLogger()
    tolerance = 1e-6

    newton_value, newton_iterations = newton_method(
        _function, [0., 0.], tolerance
    )
    x, y = newton_value
    minimum_val = (
            4 * np.power(x, 2) - 0.5 * x * y + 0.5 * np.power(y, 2) - 2.2 *
            x - 1.8 * y)
    _log.info(
        "Newton:\t\t\tMinimum of f(x, y) = f(%.6f, %.6f) = %.6f", x, y,
        minimum_val
    )
    _log.info("Newton\t\t\tIterations:\t%d", newton_iterations)

    descend_result, descend_iterations = steepest_descend_method(
        lambda vector: _function(*vector), [0., 0.]
    )
    descend_value = _function(*descend_result)
    _log.info(
        "Steepest Desent:\tMinimum of f(x, y) = f(%.6f, %.6f) = %.6f",
        *descend_result, descend_value
    )
    _log.info("Steepest Descent:\tIterations:\t%d", descend_iterations)

    figure = plt.figure()
    axis = figure.add_subplot(1, 1, 1, projection='3d')
    x, y = np.meshgrid(
        np.linspace(-5, 5, 100),
        np.linspace(-5, 5, 100)
    )
    z = (4 * np.power(x, 2) - 0.5 * x * y + 0.5 * np.power(
        y, 2
    ) - 2.2 * x - 1.8 * y)
    axis.plot_surface(x, y, z)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('f(x,y)')
    plt.show()

    figure, axis = plt.subplots(1, 1)
    axis.contour(x, y, z, levels=20)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('f(x,y)')
    plt.show()
