import argparse
import csv
import random

import numpy as np
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument("-file")

args = parser.parse_args()
file = args.file or "./data/Test14.csv"

points = []
with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        points.append(float("".join(row)))
points.sort()



def test_hypothesis(data: np.array, alpha: float):
    mean = np.mean(data)
    std_dev = np.std(data)
    theoretical_values = stats.norm(mean, std_dev)

    ks_statistic = stats.kstest(
        data,
        theoretical_values.cdf
    )

    cvm_statistic = stats.cramervonmises(
        data,
        theoretical_values.cdf
    )

    chi2_statistic = stats.chisquare(
        data
    )

    print(f'{ks_statistic.statistic=}')
    if ks_statistic.statistic < alpha:
        print(
            "Отвергаем основную гипотезу с использованием критерия Колмогорова-Смирнова"
        )
    else:
        print(
            "Принимаем основную гипотезу с использованием критерия Колмогорова-Смирнова"
        )

    print(f'{cvm_statistic.statistic=}')
    if cvm_statistic.statistic < alpha:
        print(
            "Отвергаем основную гипотезу с использованием критерия Крамера-фон-Мизеса"
        )
    else:
        print(
            "Принимаем основную гипотезу с использованием критерия Крамера-фон-Мизеса"
        )

    print(f'{chi2_statistic.statistic=}')
    if chi2_statistic.statistic < alpha:
        print("Отвергаем основную гипотезу с использованием критерия Пирсона")
    else:
        print("Принимаем основную гипотезу с использованием критерия Пирсона")


if __name__ == '__main__':
    data = np.array(points)
    sample = random.sample(list(points), 13)
    alpha = 0.001
    print(f"k_1={len(data)}")
    test_hypothesis(data, alpha)
    print(f"k_2={len(sample)}")
    test_hypothesis(sample, alpha)
