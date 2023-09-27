import argparse
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


def encode(message: int, e: int, n: int) -> int:
    return fast_pow(message, e) % n


def decode(message: int, d: int, n: int) -> int:
    return fast_pow(message, d) % n


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n")
    parser.add_argument("-e")
    parser.add_argument("-m")
    parser.add_argument("-s")
    args = parser.parse_args()

    n = int(args.n)
    e = int(args.e)
    s = int(args.s)
    m = int(args.m)

    print(f"Параметры: {n=}, {e=}")
    print(f"Сообщение: ({m}, {s})")
    if encode(m, e, n) == s:
        print(f"Проверка подлинности для ({m}, {s}) прошла успешно")
    else:
        print(f"Проверка подлинности для ({m}, {s}) завершилась неудачей")
