import argparse
import csv
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from prettytable import PrettyTable



def read_points(path: str) -> list[str]:
    points = []
    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            points.append(float(''.join(row)))
    
    return points

def solve(points: list[float]):
    alpha = 0.1
    sample_size = len(points)

    sample_mean = np.mean(points)
    sample_std = np.std(points)

    null_hypothesis_mean = sample_mean 
    t_statistics =  stats.ttest_1samp(points, sample_mean)

    p_value = 2 * (1 - stats.t.cdf(np.abs(t_statistics), df=sample_size - 1))
    
    alternative_hypothesis_means = np.linspace(null_hypothesis_mean, null_hypothesis_mean + 5, 5)

    power_values = np.array([
        1 - stats.t.cdf((null_hypothesis_mean - alt_mean) / (sample_std / np.sqrt(sample_size)), df=sample_size - 1)
        for alt_mean in alternative_hypothesis_means
    ])

    plt.figure()
    plt.plot(alternative_hypothesis_means, power_values, color='k', label='Мощность критерия')
    plt.xlabel('Значение параметра распределения')
    plt.ylabel('Мощность критерия')
    plt.axhline(alpha, color='r', label=f'$\\alpha = {alpha}$')
    plt.ylim(0, 1.1)
    plt.legend()
    plt.show()

    table = PrettyTable()
    table.add_column('Значение параметра распределения', alternative_hypothesis_means)
    table.add_column('Мощность критерия', power_values)
    table.add_column('Ошибка II рода', 1 - power_values)
    print(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-file')

    args = parser.parse_args()
    file = args.file or './data/Test14.csv'

    points = read_points(file)
    print('Полный объём исходных данных:')
    solve(points)

    points = np.random.choice(points, 25)
    print('Любые 25 значений из заданной выборки:')
    solve(points)
