import argparse
import csv

import numpy as np
import prettytable

import matplotlib.pyplot as plt
import statistics as st
from scipy.stats import gaussian_kde


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-file") or "./data/Test14.csv"

    args = parser.parse_args()
    file = args.file

    points = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            points.append(float("".join(row)))
    points.sort()

    min_point = points[0]
    max_point = points[-1]
    points_range = max_point - min_point

    print(f"Размах выборки: {points_range:.2f}")

    num_bins = 1 + int(np.ceil(np.log2(len(points))))
    print(f"Количество интервалов: {num_bins}")

    step = points_range / num_bins
    print(f"Длина интервала: {step:.2f}")

    _bins = []
    for i in range(num_bins):
        current_min = min_point + i * step
        current_max = min_point + (i + 1) * step
        current_range = (current_min, current_max)
        count = len(
            list(
                filter(
                    lambda x: current_min <= x <= current_max, points
                )
            )
        )
        current_average = (current_max + current_min) / 2.
        _bins.append(
            {
                "average": round(current_average, 4),
                "minimum": round(current_min, 4),
                "maximum": round(current_max, 4),
                "count": round(count, 4)
            }
        )

    table = prettytable.PrettyTable()
    table.field_names = [
        "Номер промежутка", "a_{i-1}", "a_i", "n_i",
        "Средняя точка промежутка"
    ]

    index = 1
    for bin in _bins:
        table.add_row([index := index + 1, bin["minimum"], bin["maximum"],
            bin["count"], bin["average"]])

    print(table)

    print(f"Выборочное среднее: {np.mean(points):.2f}")
    print(f"Медиана: {np.median(points):.2f}")
    print(f"Мода: {st.mode(points):.2f}")
    print(f"Размах выборки: {max(points) - min(points):.2f}")
    print(f"Выборочная дисперсия: {np.var(points):.2f}")
    print(f"Стандартное отклонение выборки: {np.sqrt(np.var(points)):.2f}")
    print(f"Коэффициент вариации: "
          f"{np.sqrt(np.var(points)) / np.mean(points) / 100:.2f}")

    plt.hist(
        points, color="grey", edgecolor="black", bins=num_bins, range=(
            min_point,
            max_point), alpha=0.5, density=True, label="Гистограмма"
    )
    centers = [bin["average"] for bin in _bins]
    _bins_plot = [bin["count"] / 49 for bin in _bins]
    plt.plot(centers, _bins_plot, color="black")

    plt.show()


    def normal_distribution(x):
        return 1 / np.sqrt(2 * np.pi) / np.sqrt(np.var(points)) * (
            np.exp(-1 / 2 * (
                    (x - np.mean(points)) / np.sqrt(np.var(points))) ** 2
            )
        )

    kde = gaussian_kde(points)
    xs = np.linspace(min_point, max_point, 100)
    plt.hist(
        points, color="grey", edgecolor="black", bins=num_bins, range=(
            min_point,
            max_point), alpha=0.5, density=True, label="Гистограмма"
    )
    plt.plot(xs, [kde(x) for x in xs], color="red",
        label="Усреднённая ядерная оценка")
    plt.plot(xs, [normal_distribution(x) for x in xs], color="green",
        label="Параметрическая оценка")
    plt.legend()

    plt.show()

    table = prettytable.PrettyTable()
    table.field_names = [
        "z_i", "n_i", "f_Г(x)", "f_УЯ(x)", "f_П(x)", "(f_УЯ(x)-f_Г(x))^2",
        "(f_П(x)-f_Г(x))^2",
    ]

    index = 1
    for bin in _bins:
        current_average = bin["average"]
        current_count = bin["count"]
        current_histogram = round(current_count / len(points) / 0.5, 4)
        current_kde = round(float(kde(current_average)), 4)
        current_parametric = round(normal_distribution(current_average), 4)
        diff_kde = round((current_kde - current_histogram) ** 2, 4)
        diff_parametric = round((current_parametric - current_histogram) ** 2, 4)
        table.add_row([
            current_average, current_count, current_histogram,
            current_kde, current_parametric, diff_kde, diff_parametric
        ])

    print(table)
