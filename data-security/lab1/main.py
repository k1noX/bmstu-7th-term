import argparse
import json

LOWERCASE = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
UPPERCASE = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def shift(text: str, symbols: str, n: int) -> str:
    index = symbols.find(text)
    if index + n < len(symbols):
        return symbols[index + n]
    else:
        return symbols[(index + n) % len(symbols)]


def back_shift(text: str, symbols: str, n: int) -> str:
    index = symbols.find(text)
    if index - n >= 0:
        return symbols[index - n]
    else:
        return symbols[(index - n) % len(symbols)]


def encrypt(text: str, n: int) -> str:
    result = ""
    for i in range(len(text)):
        if text[i].isupper():
            result += shift(text[i], UPPERCASE, n)
        elif text[i].islower():
            result += shift(text[i], LOWERCASE, n)
        else:
            result += text[i]
    return result



def decrypt(text: str, n: int) -> str:
    result = ""
    for i in range(len(text)):
        if text[i].isupper():
            result += back_shift(text[i], UPPERCASE, n)
        elif text[i].islower():
            result += back_shift(text[i], LOWERCASE, n)
        else:
            result += text[i]
    return result


def load_key_from_file(path: str) -> int:
    with open(path) as file:
        return json.loads(file.read())["key"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("text")
    parser.add_argument(
        "-d", "--decrypt",
        action="store_true"
    )
    args = parser.parse_args()

    key = load_key_from_file(args.path or "key.json")
    if args.decrypt:
        print("Расшифрованный текст:", decrypt(args.text, key))
    else:
        print("Зашифрованный текст:", encrypt(args.text, key))
