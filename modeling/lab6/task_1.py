import math
import typing

import numpy as np
import matplotlib.pyplot as plt


def is_prime(n: typing.Union[int, float]) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime_numbers() -> list[int]:
    primes = [num for num in range(100, 1000) if is_prime(num)]
    return primes


def calculate_errors(
        data: np.array,
        expected_mean: float,
        expected_var: float,
        expected_std_dev: float
) -> tuple:
    mean = np.mean(data)
    variance = np.var(data)
    std_dev = np.std(data)

    relative_error_mean = abs(mean - expected_mean) / expected_mean
    relative_error_var = abs(variance - expected_var) / expected_var
    relative_error_std_dev = abs(std_dev - expected_std_dev) / expected_std_dev

    return relative_error_mean, relative_error_var, relative_error_std_dev


if __name__ == '__main__':
    prime_numbers = generate_prime_numbers()

    print(f"Среднее выборочное: {np.mean(prime_numbers):.2f}")
    print(f"Выборочная дисперсия: {np.var(prime_numbers):.2f}")
    print(f"Выборочное стандартное отклонение: {np.std(prime_numbers):.2f}")

    print()

    expected_mean = 550
    expected_var = 67500
    expected_std_dev = math.sqrt(expected_var)

    relative_errors = calculate_errors(
        prime_numbers,
        expected_mean,
        expected_var,
        expected_std_dev
    )

    print(
        f"Относительная погрешность по математическому ожиданию: "
        f"{relative_errors[0] * 100:.2f}%"
    )
    print(
        f"Относительная погрешность по дисперсии: "
        f"{relative_errors[1] * 100:.2f}%"
    )
    print(
        f"Относительная погрешность по стандартному отклонению: "
        f"{relative_errors[2] * 100:.2f}%"
    )
    Zx = np.random.choice(prime_numbers, size=100)
    Zy = np.random.choice(prime_numbers, size=100)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.hist(Zx, bins=20, color='skyblue', edgecolor='black')
    plt.title('Гистограмма Zx')
    plt.xlabel('Значения')
    plt.ylabel('Частота')

    plt.subplot(1, 2, 2)
    plt.hist(Zy, bins=20, color='salmon', edgecolor='black')
    plt.title('Гистограмма Zy')
    plt.xlabel('Значения')
    plt.ylabel('Частота')

    plt.tight_layout()
    plt.show()
