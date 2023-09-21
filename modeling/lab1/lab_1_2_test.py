import numpy as np
import scipy.optimize as optimize
import sympy as sp
from IPython.display import clear_output
from sympy import *


def f(x, t):
    return np.exp(x + t) - np.exp(np.power(t, 2)) - 3 * np.cos(x)


def func_fx(t):
    return optimize.fsolve(f, 0, args=(t))


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
    fx1 = func_fx(x1)
    fx2 = func_fx(x2)
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
    fx1 = func_fx(x1)
    fx2 = func_fx(x2)
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


def golden_search(xl, xu, mode, et):
    it = 0
    e = 1
    while e >= et:
        new_x = update_interior(xl, xu)
        x1 = new_x[0]
        x2 = new_x[1]
        fx1 = func_fx(x1)
        fx2 = func_fx(x2)
        label = check_pos(x1, x2)
        clear_output(wait=True)

        # SELECTING AND UPDATING BOUNDARY-INTERIOR POINTS
        if mode == 'max':
            new_boundary = find_max(xl, xu, x1, x2, label)
        elif mode == 'min':
            new_boundary = find_min(xl, xu, x1, x2, label)
        else:
            print('Please define min/max mode')
            break  # exit if mode not min or max
        xl = new_boundary[0]
        xu = new_boundary[1]
        xopt = new_boundary[2]

        it += 1
        print('Iteration: ', it)
        r = (np.sqrt(5) - 1) / 2  # GOLDEN RATIO
        e = abs(xu - xl) * (1 / r)  # Error
        print('Error:', e)
        if mode == 'max':
            print('Max:', fx2, x2)
        else:
            print('Min:', fx2, x2)


def test(t):
    return optimize.fsolve(f, 1, args=(t))


# EXECUTING GOLDEN SEARCH FUNCTION
golden_search(0, 2, 'max', 0.0005)

# EXECUTING GOLDEN SEARCH FUNCTION
golden_search(0, 2, 'min', 0.0005)

x, t = np.meshgrid(np.linspace(0, 2, 100), np.linspace(0, 2, 100))
var("x t")
plot_implicit(Eq(x ** 4 - 10 * sp.sin(t) + 5 * x, 0))
