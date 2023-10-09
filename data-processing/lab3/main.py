# X - выборка из распределения \xi_k, где k = 3. Найти оценку параметра k,
# считая его неизвестным. Метод моментов реализовать с помощью моментов 1-го и
# 2-го порядков.

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2


def get_distribution_sample() -> list:
    k = 3
    n = 100
    xs = chi2(k)
    ys = xs.rvs(n)
    return ys


def get_distribution_mean(k: int) -> float:
    return chi2(k).mean()


def get_distribution_variance(k: int) -> float:
    return chi2(k).var()


if __name__ == "__main__":
    ys = get_distribution_sample()

    sample_mean = np.mean(ys)
    sample_variance = np.var(ys)

    print("Выборочное среднее:", sample_mean)
    print("Выборочная дисперсия:", sample_variance)

    differences = []

    k = sample_variance / 2
    mean = get_distribution_mean(k)
    variance = get_distribution_variance(k)
    print(f"Математическое ожидание chi({k=}):", mean)
    print(f"Дисперсия chi({k=}):", variance)

    plt.hist(ys, density=True, label="гистограмма")
    xs = np.arange(0, 16, 0.001)
    plt.plot(
        xs, chi2.pdf(xs, df=k), label="$\chi^2_{" + f"{k:.2f}" + "}$",
        color="#fe0000"
    )
    plt.plot(
        xs, chi2.pdf(xs, df=3), label="$\chi^2_{3}$", color="#0bff01"
    )
    plt.title("Точечная оценка по 2-му моменту")
    plt.legend()
    plt.show()

    k = sample_mean
    mean = get_distribution_mean(k)
    variance = get_distribution_variance(k)
    print(f"Математическое ожидание chi({k=}):", mean)
    print(f"Дисперсия chi({k=}):", variance)

    plt.hist(ys, density=True, label="гистограмма")
    xs = np.arange(0, 16, 0.001)
    plt.plot(
        xs, chi2.pdf(xs, df=k), label="$\chi^2_{" + f"{k:.2f}" + "}$",
        color="#fe0000"
    )
    plt.plot(
        xs, chi2.pdf(xs, df=3), label="$\chi^2_{3}$", color="#0bff01"
    )
    plt.title("Точечная оценка по 1-му моменту")
    plt.legend()
    plt.show()
