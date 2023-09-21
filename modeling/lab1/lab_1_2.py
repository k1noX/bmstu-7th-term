#   3.5
"""
Функция x(t) задана неявно уравнением F(x,t).
Построить график зависимости функции на заданном отрезке
и найти ee минимум и максимум с точностью.
    e**(x+t)-e**(t**2)-3*cos(x)
    t_1=0, t_2=2, x_1=0, x_2=2
    Деление отрезка пополам
"""
import logging
import sys
import typing as _t

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


def _function(t: float, x: float) -> float:
    return np.exp(x + t) - np.exp(np.power(t, 2)) - 3 * np.cos(x)


def _function_of_t(x: float):
    f = lambda x, t: _function(t, x)
    return optimize.fsolve(
        f, 0, args=(x)
    )


def _function_of_x(t: float):
    f = lambda t, x: _function(t, x)
    return optimize.fsolve(
        f, 0, args=(t)
    )


def _first_derivative_x(t: float, x: float) -> float:
    return np.exp(x + t) + 3 * np.sin(x)


def _first_derivative_t(t: float, x: float) -> float:
    return -2 * t * np.exp(np.power(t, 2)) + np.exp(t + x)


def _first_derivative(t: float, x: float) -> float:
    return _first_derivative_t(t, x) / _first_derivative_x(t, x)


class Node:
    def __init__(
            self, t: float, x: float, next_t: _t.Optional["Node"] = None,
            next_x: _t.Optional["Node"] = None
    ):
        self.t = t
        self.x = x
        self.next_t = next_t
        self.next_x = next_x

    def __repr__(self):
        return f"Node (t={self.t:.6f}, x={self.x:.6f})"


def bisection_method(
        functions: _t.List[_t.Callable[[float, float], float]],
        start: Node, end: Node, tolerance: float
) -> _t.List[Node]:
    for x, t in [
        [start.t, start.x], [start.t, end.x], [end.t, start.x], [end.t, end.x]
    ]:
        if all(abs(f(t, x)) < tolerance for f in functions):
            return [Node(t, x)]

    graph = Node(start.t, start.x)

    temp = Node(end.t, start.x)
    graph.next_t = temp

    temp = Node(start.t, end.x)
    graph.next_x = temp

    temp = Node(end.t, end.x)
    graph.next_t.next_x = temp

    return bisection(graph, functions, tolerance)


def bisection(
        node: Node, functions: _t.List[_t.Callable[[float, float], float]],
        tolerance: float
) -> _t.List[_t.Union[None, Node]]:
    n10 = node.next_t
    n11 = n10.next_x
    n01 = node.next_x

    corners = [
        [f(n.t, n.x) for n in
            [node, n10, n11, n01]] for f in functions
    ]
    are_all_signs_same = [len(set(np.sign(c))) <= 1 for c in corners]
    if all(are_all_signs_same):
        return []

    start_m_t = node.t
    start_m_x = node.x
    end_m_t = n11.t
    end_m_x = n11.x
    center_m_t = (start_m_t + end_m_t) / 2
    center_m_x = (start_m_x + end_m_x) / 2

    if end_m_t - start_m_t < 1e-10 or \
            end_m_x - start_m_x < 1e-10:
        return []

    for t, x in [
        [end_m_t, center_m_x], [center_m_t, end_m_x],
        [center_m_t, start_m_x], [start_m_t, center_m_x],
        [center_m_t, center_m_x]
    ]:
        if all(abs(f(t, x)) < tolerance for f in functions):
            return [Node(t, x)]

    temp = Node(end_m_t, center_m_x, next_x=n11)
    n10.next_x = temp

    temp = Node(center_m_t, end_m_x, next_t=n11)
    n01.next_t = temp

    temp = Node(center_m_t, start_m_x, next_t=n10)
    node.next_t = temp

    temp = Node(start_m_t, center_m_x, next_x=n01)
    node.next_x = temp

    temp = Node(center_m_t, center_m_x, next_t=n10.next_x, next_x=n01.next_t)
    node.next_t.next_x = temp
    node.next_x.next_t = temp
    node.next_x.next_t = temp

    return [
        *bisection(node, functions, tolerance),
        *bisection(node.next_t, functions, tolerance),
        *bisection(node.next_x, functions, tolerance),
        *bisection(node.next_t.next_x, functions, tolerance)
    ]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _log = logging.getLogger()

    t_1 = 0
    t_2 = 2
    x_1 = 0
    x_2 = 2
    tolerance = 1e-6

    sys.setrecursionlimit(1000)
    nodes = bisection_method(
        [lambda _t, _x: _first_derivative(_x, _t)], Node(t_1, x_1),
        Node(t_2, x_2), tolerance
    )
    min_x = nodes[0].x

    _log.info("\tMinimum of x(t) = x(%.6f) = %.6f", min_x, *_function_of_x(
        min_x))

    delta = 0.025
    xrange = np.arange(x_1, x_2, delta)
    trange = np.arange(t_1, t_2, delta)
    ts, xs = np.meshgrid(trange, xrange)

    F = _function(ts, xs)

    plt.contour(ts, xs, F, [0])
    plt.xlabel("T")
    plt.ylabel("X")
    plt.show()
