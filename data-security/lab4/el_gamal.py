import argparse
import math
from typing import Union


def fast_pow(x: int, y: int) -> Union[float, int]:
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = fast_pow(x, y // 2)
    p *= p
    if y % 2:
        p *= x
    return p


def reverse_element(f: int, d: int) -> int:
    X = [1, 0, f]
    Y = [0, 1, d]
    while True:
        if Y[2] == 0:
            raise Exception()
        elif Y[2] == 1:
            return Y[1]
        else:
            q = X[2] // Y[2]
            t = [0, 0, 0]
            for i in range(0, len(t)):
                t[i] = X[i] - q * Y[i]
                X[i] = Y[i]
                Y[i] = t[i]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    parser.add_argument("-g")
    parser.add_argument("-x")
    parser.add_argument("-k")
    parser.add_argument("-m")
    args = parser.parse_args()

    p = int(args.p)
    g = int(args.g)
    x = int(args.x)
    k = int(args.k)
    m = int(args.m)
    y = math.pow(g, x) % p
    a = math.pow(g, k) % p
    f = p - 1

    print(f"Секретные параметры: {x=}, {k=}")
    print(f"Хэш сообщения: {m=}")

    kr = reverse_element(f, k)
    b = (kr * (m - x * a)) % f

    if ((fast_pow(y, a) * fast_pow(a, b)) % p) == (fast_pow(g, m) % p):
        print("Проверка подлинности прошла успешно")
    else:
        print("Проверка подлинности завершилась неудачей")
