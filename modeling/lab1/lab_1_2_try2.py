"""
Функция x(t) задана неявно уравнением F(x,t).
Построить график зависимости функции на заданном отрезке
и найти ee минимум и максимум с точностью.
    e**(x+t)-e**(t**2)-3*cos(x)
    t_1=0, t_2=2, x_1=0, x_2=2
    Деление отрезка пополам
"""

import typing as _t

import numpy as np
import scipy.optimize as optimize


def _function(t: float, x: float) -> float:
    return np.exp(x + t) - np.exp(np.power(t, 2)) - 3 * np.cos(x)


def _first_derivative(t: float, x: float) -> float:
    return np.exp(x + t) - 2 * t * np.exp(np.power(t, 2))


def _function_of_t(t: float):
    f = lambda t, x: _function(t, x)
    return optimize.fsolve(
        f, 0,
        args=(t)
    )


def _first_derivative_of_t(t: float):
    f = lambda t, x: _first_derivative(t, x)
    return optimize.fsolve(
        f, 0,
        args=(t)
    )


def gradient(
        function: _t.Callable[[float], float],
        current: float,
        tolerance: float = 1e-6
) -> np.array:
    return optimize.approx_fprime(current, function, tolerance ** 2)


def check_pos(x1, x2):
    if x2 < x1:
        label = 'right'
    else:
        label = ''
    return label


def update_interior(xl, xu):
    d = ((np.sqrt(5) - 1) / 2) * (xu - xl)
    x1 = xl + d
    x2 = xu - d
    return x1, x2


def find_max(xl, xu, x1, x2, label):
    fx1 = _function_of_t(x1)
    fx2 = _function_of_t(x2)
    if fx2 > fx1 and label == 'right':
        xl = xl
        xu = x1
        new_x = update_interior(xl, xu)
        x1 = new_x[0]
        x2 = new_x[1]
        xopt = x2
    else:
        xl = x2
        xu = xu
        new_x = update_interior(xl, xu)
        x1 = new_x[0]
        x2 = new_x[1]
        xopt = x1
    return xl, xu, xopt


def find_min(xl, xu, x1, x2, label):
    fx1 = _function_of_t(x1)
    fx2 = _function_of_t(x2)
    if fx2 > fx1 and label == 'right':
        xl = x2
        xu = xu
        new_x = update_interior(xl, xu)
        x1 = new_x[0]
        x2 = new_x[1]
        xopt = x1
    else:
        xl = xl
        xu = x1
        new_x = update_interior(xl, xu)
        x1 = new_x[0]
        x2 = new_x[1]
        xopt = x2
    return xl, xu, xopt


def bisection_method(
        function: _t.Callable[[float], float], start: float,
        end: float, tolerance: float
) -> float:
    if np.sign(function(start)) == np.sign(function(end)):
        raise Exception("Начало и конец не должны совпадать")
    midpoint = (start + end) / 2

    if np.abs(function(midpoint)) < tolerance:
        return midpoint
    elif np.sign(function(start)) == np.sign(function(midpoint)):
        return bisection_method(function, midpoint, end, tolerance)
    elif np.sign(function(end)) == np.sign(function(midpoint)):
        return bisection_method(function, start, midpoint, tolerance)


def golden_search(xl, xu, mode, et):
    it = 0
    e = 1
    while e >= et:
        new_x = update_interior(xl, xu)
        x1 = new_x[0]
        x2 = new_x[1]
        fx1 = _function_of_t(x1)
        fx2 = _function_of_t(x2)
        label = check_pos(x1, x2)

        if mode == 'max':
            new_boundary = find_max(xl, xu, x1, x2, label)
        elif mode == 'min':
            new_boundary = find_min(xl, xu, x1, x2, label)
        else:
            print('Please define min/max mode')
        xl = new_boundary[0]
        xu = new_boundary[1]
        xopt = new_boundary[2]

        it += 1
        print('Iteration: ', it)
        r = (np.sqrt(5) - 1) / 2
        e = abs(xu - xl) * (1 / r)  # Error
        print('Error:', e)
        if mode == 'max':
            print('Max:', fx2, x2)
        else:
            print('Min:', fx2, x2)


tolerance = 1e-6
# EXECUTING GOLDEN SEARCH FUNCTION
golden_search(0, 2, 'max', 1e-6)
t = bisection_method(
    _first_derivative_of_t, 0, 2,
    tolerance
)
print("VALUE", t)
print("X=", _function_of_t(t))
print(_function(t, _function_of_t(t)))

x, t = np.meshgrid(np.linspace(0, 2, 100), np.linspace(0, 2, 100))
