# RSA

import argparse
import math
import typing as _t

RUSSIAN_ALPHABET = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
    'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
    'э', 'ю', 'я'
]


def fast_pow(x: int, y: int) -> float:
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = fast_pow(x, y // 2)
    p *= p
    if y % 2:
        p *= x
    return p


def generate_keys(p: int, q: int) -> _t.Tuple[int, int, int]:
    n = p * q
    euler = (p - 1) * (q - 1)

    e = 0
    i = 2
    while i < euler:
        e = math.gcd(euler, i)
        if e == 1:
            e = i
            break
        i += 1

    d = 0
    i = 2
    while i < n:
        if (i * e) % euler == 1:
            d = i
            break
        i += 1

    return e, d, n


def encode_number(number: int, e: int, n: int) -> float:
    return fast_pow(number, e) % n


def decode_number(number: int, d: int, n: int) -> float:
    return fast_pow(number, d) % n


def encode_message(message: str, e: int, n: int) -> list:
    iteration = 0
    encoded_message: list = [None] * len(message)

    for letter in message:
        try:
            index = RUSSIAN_ALPHABET.index(letter) + 1
            encoded_message[iteration] = encode_number(index, e, n)
        except ValueError:
            encoded_message[iteration] = letter
        iteration += 1

    return encoded_message


def decode_message(message: list, d: int, n: int) -> str:
    iteration = 0
    decoded_message: list = [""] * len(message)

    for letter in message:
        try:
            current = decode_number(letter, d, n)
            decoded_message[iteration] = RUSSIAN_ALPHABET[current - 1]
        except TypeError:
            decoded_message[iteration] = letter
        iteration += 1

    return "".join(decoded_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    parser.add_argument("-q")
    parser.add_argument("-message")
    args = parser.parse_args()

    p = int(args.p)
    q = int(args.q)
    message = args.message

    e, d, n = generate_keys(p, q)
    encoded = encode_message(message, e, n)
    print("Encoded message:", encoded)
    decoded = decode_message(encoded, d, n)
    print("Decoded message:", decoded)
