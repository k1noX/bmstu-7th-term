import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from scipy.stats import norm


def get_test_power(
        data: list[float], theta_0: float, alpha: float, theta: float,
        sample_size: int
) -> float:
    critical_value = norm.ppf(1 - alpha)
    standard_error = np.std(data) / np.sqrt(sample_size)
    critical_region = (
        theta_0 - critical_value * standard_error,
        theta_0 + critical_value * standard_error
    )
    power = 1 - norm.cdf(critical_region[1], theta, standard_error) + norm.cdf(
        critical_region[0], theta, standard_error
    )
    return power


def read_points(path: str) -> list[float]:
    points = []

    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            points.append(float(''.join(row)))

    return points


def solve(points: list[float]):
    alpha = 0.1
    theta_0 = np.mean(points)
    delta = np.std(points) / np.sqrt(len(points))
    thetas = [theta_0 + i * delta for i in range(1, 6)]

    small_sample_power = np.array(
        [
            get_test_power(
                points, theta_0, alpha, theta, 25
            ) for theta in thetas
        ]
    )
    full_sample_power = np.array(
        [
            get_test_power(
                points, theta_0, alpha, theta, len(points)
            ) for theta in thetas
        ]
    )

    table = PrettyTable()
    table.add_column('Значение параметра распределения', thetas)
    table.add_column('Мощность критерия', small_sample_power)
    table.add_column('Ошибка II рода', 1 - small_sample_power)
    print('Любые 25 из заданной выборки:')
    print(table)

    table = PrettyTable()
    table.add_column('Значение параметра распределения', thetas)
    table.add_column('Мощность критерия', full_sample_power)
    table.add_column('Ошибка II рода', 1 - full_sample_power)
    print('Все значения выборки:')
    print(table)

    plt.figure(figsize=(10, 5))
    plt.plot(thetas, small_sample_power, label='Мощность критерия при $N=25$')
    plt.plot(
        thetas, full_sample_power, label=f'Мощность критерия $N={len(points)}$'
    )
    plt.xlabel('Значение параметра распределения')
    plt.ylabel('Мощность критерия')
    plt.axhline(
        alpha, color='red',
        label=f"$\\alpha={alpha}$"
    )
    plt.legend()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-file')

    args = parser.parse_args()
    file = args.file or './data/Test14.csv'

    points = read_points(file)
    solve(points)
