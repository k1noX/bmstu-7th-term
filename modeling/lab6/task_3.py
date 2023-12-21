import math
import scipy.stats as sps


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


if __name__ == '__main__':
    counts = [100, 500, 1000]
    for count in counts:
        print(f"При размере выборки равном: {count}")
        rnd = LinearCongruentialGenerator(95, int(8.44 * 10 ** 6))
        x = rnd.generate_float_number_array(count)
        F0 = sps.expon.cdf(x)
        H0 = sps.kstest(x, F0, N=count)[1]
        if H0 < 0.95:
            print(
                f"При экспоненциальном распределении и уровне значимости 0.05, "
                f"нулевая гипотеза подтверждается: p = {H0}")
        else:
            print(
                f"При экспоненциальном распределении и уровне значимости 0.05, "
                f"нулевая гипотеза не подтверждается: p = {H0}")
        F1 = sps.uniform.cdf(x)
        H1 = sps.kstest(x, F1, N=count)[1]
        if H1 < 0.95:
            print(f"При равномерном распределении и уровне значимости 0.05, "
                  f"нулевая гипотеза подтверждается: p = {H1}")
        else:
            print(f"При равномерном распределении и уровне значимости 0.05, "
                  f"нулевая гипотеза не подтверждается: p = {H1}")
        F2 = sps.norm.cdf(x)
        H2 = sps.kstest(x, F2, N=count)[1]
        if H2 < 0.95:
            print(f"При нормальном распределении и уровне значимости 0.05, "
                  f"нулевая гипотеза подтверждается: p = {H2}")
        else:
            print(f"При нормальном распределении и уровне значимости 0.05, "
                  f"нулевая гипотеза не подтверждается: p = {H2}")
        print()
