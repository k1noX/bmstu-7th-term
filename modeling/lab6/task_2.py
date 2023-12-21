import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


class LinearCongruentialGenerator:
    @classmethod
    def generate_primes(cls, n: int) -> list[int]:
        sieve = [True] * n
        for i in range(3, int(n ** 0.5) + 1, 2):
            if sieve[i]:
                sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
        return [2] + [i for i in range(3, n, 2) if sieve[i]]

    def __find_M(self, N):
        m = self.generate_primes(N)
        M = m[-1]
        return M

    def __find_A(self, M):
        a = int(M * (1 / 2 - math.sqrt(3) / 6))
        if a % 2 == 0:
            a += 1
        if a % 8 == 5:
            if math.gcd(a, M) == 1:
                return a
        i = 1
        while True:
            a1 = a + 2 * i
            if a1 % 8 == 5:
                if math.gcd(a1, M) == 1:
                    if a1 < (M - math.sqrt(M)):
                        return a1
            a2 = a - 2 * i
            if a2 % 8 == 5:
                if math.gcd(a2, M) == 1:
                    if a2 > (M // 100):
                        return a2
            i += 1

    def __init__(self, R0, N, c=0):
        self.__c = int(c)
        self.__Rk = int(R0)
        M = self.__find_M(N)
        self.__M = int(M)
        a = self.__find_A(M)
        self.__a = a

    def generate_int_number(self):
        number = (self.__a * self.__Rk + self.__c) % self.__M
        self.__Rk = number
        return number

    def generate_float_number(self):
        number = (self.__a * self.__Rk + self.__c) % self.__M
        self.__Rk = number
        number /= self.__M
        return number

    def generate_int_number_array(self, count):
        array = []
        for i in range(count):
            number = (self.__a * self.__Rk + self.__c) % self.__M
            self.__Rk = number
            array.append(number)
        return array

    def generate_float_number_array(self, count):
        array = []
        for i in range(count):
            number = (self.__a * self.__Rk + self.__c) % self.__M
            self.__Rk = number
            number /= self.__M
            array.append(number)
        return array


def print_period_sequence(N, order):
    m = LinearCongruentialGenerator.generate_primes(N)
    R0 = m[order]
    rnd = LinearCongruentialGenerator(R0, N)
    base = rnd.generate_int_number()
    i = 0
    while True:
        i += 1
        if rnd.generate_int_number() == base:
            break
    print(
        f"При N={N} и R0=m({order})={R0}\nПериод формируемой случайной последовательности равен: {i}")


def print_distribution_parameters(N: int, order: int):
    m = LinearCongruentialGenerator.generate_primes(N)
    R0 = m[order]
    rnd = LinearCongruentialGenerator(R0, N)
    x = rnd.generate_float_number_array(500)
    mf = np.mean(x)
    print(f"Среднее выборочное: {mf:.2f}")
    sf2 = np.var(x)
    print(f"Выборочная дисперсия: {sf2:.2f}")
    sf = np.std(x)
    print(f"Выборочное стандартное отклонение: {sf:.2f}")
    m = 0.5
    Dm = abs((mf - m) / m) * 100
    print(f"Относительная погрешность по математическому ожиданию: {Dm:.2f}%")
    d = 1 / 12
    Dd = abs((sf2 - d) / d) * 100
    print(f"Относительная погрешность по дисперсии: {Dd:.2f}%")
    sd = np.sqrt(d)
    Ds = abs((sf - sd) / sd) * 100
    print(f"Относительная погрешность по стандартному отклонению: {Ds:.2f}%")


def generate_histogram(N: int, order: int, size: int):
    m = LinearCongruentialGenerator.generate_primes(N)
    R0 = m[order]
    rnd = LinearCongruentialGenerator(R0, N)
    x = rnd.generate_float_number_array(size)
    plt.hist(x, bins=int(size / 10), edgecolor='black', linewidth=1)
    plt.title(f"Гистограмма полученного распределения случайных чисел\n"
              f"при {N=} и m({order})")
    plt.xlabel("Значение")
    plt.ylabel("Частота")
    plt.show()


def generate_cdf(N, order, size):
    m = LinearCongruentialGenerator.generate_primes(N)
    R0 = m[order]
    rnd = LinearCongruentialGenerator(R0, N)
    a = 0
    b = 1
    n = size
    x = np.linspace(a, b, n)
    y = sorted(rnd.generate_float_number_array(n))
    plt.plot(
        x, y, "-g",
        label=f"Эмпирическая функция распределения, n={len(x)}"
    )
    y = (x - a) / (b - a)
    plt.plot(x, y, "-k", label="Теоретическая функция распределения")
    y = x - 1.36 / len(x) ** (0.5)
    plt.plot(x, y, "--r", label="Доверительный интервал в 95%")
    y = x + 1.36 / len(x) ** (0.5)
    plt.plot(x, y, "--r")
    plt.title("Функция распределения\n"
              f"при {N=} и m({order})")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.show()


def generate_pdf(N: int, order: int, size: int):
    m = LinearCongruentialGenerator.generate_primes(N)
    R0 = m[order]
    rnd = LinearCongruentialGenerator(R0, N)
    a = 0
    b = 1
    n = size
    x = np.linspace(a, b, n)
    y = rnd.generate_float_number_array(n)
    plt.hist(
        y, density=True, fc="none", ec="red",
        label="Эмпирическая плотность, n = %i" % len(x)
    )
    density = gaussian_kde(y)
    density.covariance_factor = lambda: .25
    density._compute_covariance()
    plt.plot(
        x, density(x), "-g",
        label="Эмпирическая функция плотности, n = %i" % len(x)
    )
    plt.fill_between(
        x, 0, density(x), color="none", hatch='\\',
        edgecolor="b"
    )
    y = x * 0 + 1 / (b - a)
    plt.plot(x, y, "-k", label="Теоретическая функция плотности")
    plt.fill_between(x, 0, y, color="none", hatch="/", edgecolor="k")
    plt.title("Функция плотности \n"
              f"при {N=} и m({order})")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.show()


def plot_uniformity_diagram(
        first_N: float,
        first_order: int,
        second_N: float,
        second_order: int,
        count: int
):
    first_random = LinearCongruentialGenerator(first_order, first_N)
    second_random = LinearCongruentialGenerator(second_order, second_N)
    x = first_random.generate_float_number_array(count)
    y = second_random.generate_float_number_array(count)

    plt.plot(x, y, 'bo', markersize=4)
    plt.title(
        "Диаграмма оценки равномерности случайных чисел,"
        f"\nпри их количестве равном: {count}"
    )
    plt.xlabel(f"Случайные числа при N={first_N} и R0={first_order}")
    plt.ylabel(f"Случайные числа при N={second_N} и R0={second_order}")
    plt.show()


if __name__ == '__main__':
    Ns = [int(8.44 * 10 ** 6), int(9.55 * 10 ** 6), int(9.66 * 10 ** 6)]
    orders = [34, 35, 36]
    print()

    print_period_sequence(Ns[0], orders[0])
    print_distribution_parameters(Ns[0], orders[0])
    generate_histogram(Ns[0], orders[0], 500)
    generate_cdf(Ns[0], orders[0], 500)
    generate_pdf(Ns[0], orders[0], 500)
    print()

    print_period_sequence(Ns[1], orders[1])
    print_distribution_parameters(Ns[1], orders[1])
    generate_histogram(Ns[1], orders[1], 500)
    generate_cdf(Ns[1], orders[1], 500)
    generate_pdf(Ns[1], orders[1], 500)
    print()

    print_period_sequence(Ns[2], orders[2])
    print_distribution_parameters(Ns[2], orders[2])
    generate_histogram(Ns[2], orders[2], 500)
    generate_cdf(Ns[2], orders[2], 500)
    generate_pdf(Ns[2], orders[2], 500)
    print()

    plot_uniformity_diagram(
        Ns[0],
        LinearCongruentialGenerator.generate_primes(250)[orders[0]],
        Ns[2],
        LinearCongruentialGenerator.generate_primes(250)[orders[2]],
        500
    )
    print()
