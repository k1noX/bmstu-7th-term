# Вариант 14
#   1.14
#       3*cos(x)-sin(x)
#       a=0, b=5
#   3.5
#       e**(x+t)-e**(t**2)-3*cos(x)
#       t_1=0, t_2=2, x_1=0, x_2=2
#       Деление отрезка пополам
#   5.14
#       3*x**2+2*y**4+y*cos(exp(2*x))
#   6.14
#       a_11=4, 2a_12=-0.5, a_22=0.5, 2a_13=-2.2, 2a_23=-1.8
#       Наискорейший поиск
import logging
import sys
import typing as _t

import numpy as np


def func(x: float) -> float:
    return 3 * np.cos(x) - np.sin(x)


def derivative(x: float) -> float:
    return -3 * np.sin(x) - np.cos(x)


def second_derivative(x: float) -> float:
    return -3 * np.cos(x) + np.sin(x)


def third_derivative(x: float) -> float:
    return 3 * np.sin(x) + np.cos(x)


def get_next_x(
        x: float,
        func: _t.Callable[[float], float],
        derivative: _t.Callable[[float], float],
) -> float:
    return x - func(x) / derivative(x)


if __name__ == "__main__":
    a = 0
    b = 5
    tolerance = 1e-6
    x = (a + b) / 2
    iteration = 0
    difference = sys.float_info.max

    while difference > tolerance:
        current_x = get_next_x(x, derivative, second_derivative)
        difference = abs(x - current_x)
        x = current_x
        iteration += 1

    logging.basicConfig(level=logging.DEBUG)
    _log = logging.getLogger()
    _log.setLevel(logging.DEBUG)
    _log.info(
        "\tПолученнное значение \t %.6f - %s",
        x, "минимум" if second_derivative(x) > 0 else "максимум"
    )
    _log.info("\tКоличество итераций \t %d", iteration)
