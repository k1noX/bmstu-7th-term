import matplotlib.pyplot as plt
import prettytable


def calculate_letter_frequency(text: str):
    letters = dict()
    length = len(text)

    for letter in text:
        if not letter.isalpha():
            continue

        lowercase_letter = letter.lower()
        if lowercase_letter in letters:
            letters[lowercase_letter] += 1
        else:
            letters[lowercase_letter] = 1

    for lowercase_letter in letters:
        letters[lowercase_letter] /= length

    return letters


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


def form_translate_dict(input: list, output: list):
    result = dict(zip(input, output))

    table = prettytable.PrettyTable()
    table.field_names = ["Шифрованный текст", "Открытый текст"]
    for k in result:
        table.add_row([k, result[k]])

    print(table)
    result |= dict(
        zip([l.upper() for l in input], [l.upper() for l in output])
    )

    return str.maketrans(result)


if __name__ == "__main__":
    with open("data/input.txt", encoding="UTF8") as file:
        input_text = file.read()

    input_freq = calculate_letter_frequency(input_text.lower())

    input_freq = {k: v for k, v in
        sorted(input_freq.items(), key=lambda item: item[1], reverse=True)}

    with open("data/cypher.txt", encoding="UTF8") as file:
        cypher_text = file.read()

    cypher_freq = calculate_letter_frequency(cypher_text.lower())
    cypher_freq = {k: v for k, v in
        sorted(cypher_freq.items(), key=lambda item: item[1], reverse=True)}

    translate_dict = form_translate_dict(
        cypher_freq,
        input_freq
    )

    print("Текст в шифрованном виде:")
    print(cypher_text)

    replaced = cypher_text.translate(translate_dict)
    print("Текст с заменами:")
    print(decrypt(cypher_text, 3))

    with open("output.txt", mode="w", encoding="UTF8") as file:
        file.write(decrypt(cypher_text, 3))

    figure, (first_axis, second_axis) = plt.subplots(1, 2)
    first_axis.bar(cypher_freq.keys(), cypher_freq.values(), color='g')
    first_axis.title.set_text("Текст в шифрованном виде")

    second_axis.bar(input_freq.keys(), input_freq.values(), color='r')
    second_axis.title.set_text("Текст в открытом виде")

    plt.tight_layout()
    plt.show()
