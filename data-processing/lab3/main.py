# X - выборка из распределения \xi_k, где k = 3. Найти оценку параметра k,
# считая его неизвестным. Метод моментов реализовать с помощью моментов 1-го и
# 2-го порядков.

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma
from scipy.stats import chi2


def get_distribution_sample() -> list:
    k = 3
    n = 100
    xs = chi2(k)
    ys = xs.rvs(n)
    return ys


def get_distribution_mean(k: float) -> float:
    return chi2(k).mean()


def get_distribution_variance(k: float) -> float:
    return chi2(k).var()


def get_likelihood_value(xs: list, k: float) -> float:
    xs = np.delete(xs, 0)
    n = len(xs)
    result = (k / 2 - 1) * np.sum(np.log(xs)) - 1 / 2 * np.sum(xs) \
             - n * np.log(gamma(k / 2)) - n * k / 2 * np.log(2)
    return result


if __name__ == "__main__":
    ys = get_distribution_sample()

    sample_mean = np.mean(ys)
    sample_variance = np.var(ys)
    print("\nВыборочные показатели")

    print("Выборочное среднее:", sample_mean)
    print("Выборочная дисперсия:", sample_variance)

    k = 3
    mean = get_distribution_mean(k)
    variance = get_distribution_variance(k)

    print("\nТеоретические показатели")

    print(f"Математическое ожидание chi({k=:.2f}):", mean)
    print(f"Дисперсия chi({k=:.2f}):", variance)

    differences = []

    k = sample_variance / 2
    mean = get_distribution_mean(k)
    variance = get_distribution_variance(k)
    print("\nМетод моментов")
    print("\nТочечная оценка по 2-му моменту:")
    print(f"{k=:.2f}")
    print(f"Математическое ожидание chi({k=:.2f}):", mean)
    print(f"Дисперсия chi({k=:.2f}):", variance)

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
    print("\nТочечная оценка по 1-му моменту")
    print(f"{k=:.2f}")
    print(f"Математическое ожидание chi({k=:.2f}):", mean)
    print(f"Дисперсия chi({k=:.2f}):", variance)

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

    ks = np.arange(1, 5, 0.01)
    likelihood_values = np.array([get_likelihood_value(ys, k) for k in ks])
    max_likelihood_indices = np.argmax(likelihood_values)
    k = ks[max_likelihood_indices]

    print("\nМетод наибольшего правдоподобия")
    print(f"Наиболее правдоподобное значение параметра: {k=:.2f}")

    mean = get_distribution_mean(k)
    variance = get_distribution_variance(k)
    print(f"Математическое ожидание chi({k=:.2f}):", mean)
    print(f"Дисперсия chi({k=:.2f}):", variance)

    plt.plot(
        ks, likelihood_values, label="Функция правдоподобия $L(k)$",
        color="#0bff01"
    )
    plt.title("Функция правдоподобия $L(k)$")
    plt.show()

    plt.hist(ys, density=True, label="гистограмма")
    xs = np.arange(0, 16, 0.001)
    plt.plot(
        xs, chi2.pdf(xs, df=k), label="$\chi^2_{" + f"{k:.2f}" + "}$",
        color="#fe0000"
    )
    plt.plot(
        xs, chi2.pdf(xs, df=3), label="$\chi^2_{3}$", color="#0bff01"
    )
    plt.title("Метод максимального правдоподобия")
    plt.legend()
    plt.show()
