# Диффи-Хеллман

import argparse
import math


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q")
    parser.add_argument("-a")
    parser.add_argument("-Xa")
    parser.add_argument("-Yb")
    parser.add_argument("-k")
    args = parser.parse_args()

    q = int(args.q)
    a = int(args.a)
    Xa = int(args.Xa)
    Yb = int(args.Yb)
    k = int(args.k)

    # Xa - секретный ключ абонента 1
    # Yb - открытый ключ абонента 2
    # q - общее простое число
    # a - первообразный корень
    # K - общий секретный ключ

    Xb = math.pow(a, Xa) % q
    print("Секретный ключ Xb:", Xb)
