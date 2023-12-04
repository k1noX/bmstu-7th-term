import argparse
import csv
import random
import typing

import numpy as np
import prettytable as pt
import scipy.stats as st
from scipy.stats import norm


def ft(x):
    mean_value = np.mean(x)
    std_deviation = np.std(x, ddof=1)
    cdf_value = norm.cdf(x, loc=mean_value, scale=std_deviation)
    return cdf_value


def chi_squared_test(points: np.array, expected_frequencies=None,
        bins=None):
    if bins is None:
        bins = int(np.sqrt(len(points)))

    observed_frequencies, bin_edges = np.histogram(points, bins=bins)

    if expected_frequencies is None:
        expected_frequencies = (np.ones_like(observed_frequencies) *
                                len(points) / bins)

    chi2 = np.sum(
        (observed_frequencies - expected_frequencies) ** 2
        / expected_frequencies
    )
    dof = bins - 1

    return chi2, dof


def test_hypothesis(sample: np.array, alpha: float) -> pt.PrettyTable:
    sample = np.sort(sample)
    F_emp = np.arange(1, len(sample) + 1) / len(sample)
    F_theor = ft(sample)
    D = np.max(np.abs(F_emp - F_theor))
    W2 = np.sum((F_emp - F_theor) ** 2) + 1 / (
                12 * len(sample))  
    
    chi2, dof = chi_squared_test(sample)
    
    D_crit = st.kstwobign.ppf(1 - alpha) / np.sqrt(len(sample))  
    W2_crit = st.chi2.ppf(1 - alpha, df=1)  
    chi2_crit = st.chi2.ppf(1 - alpha, df=len(sample) - 1)  
    result = pt.PrettyTable()  
    result.field_names = ["Критерий", "Статистика", "Критическое значение",
        "Вывод"]
    result.add_row(
        ["Колмогоров", round(D, 4), round(D_crit, 4),
            "Принять" if D < D_crit else "Отклонить"]
    )
    result.add_row(
        ["Крамер-фон Мизес", round(W2, 4), round(W2_crit, 4),
            "Принять" if W2 < W2_crit else "Отклонить"]
    )
    result.add_row(
        ["Пирсон", round(chi2, 4), round(chi2_crit, 4),
            "Принять" if chi2 < chi2_crit else "Отклонить"]
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-file")

    args = parser.parse_args()
    file = args.file or "./data/Test14.csv"

    points = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            points.append(float("".join(row)))
    points = np.array(points)

    alpha = np.array([0.01, 0.05, 0.001])

    sample_k = 11
    sample = random.sample(list(points), 11)
    sample_result = []
    for a in alpha:
        sample_result.append(test_hypothesis(sample, a))

    all_points_k = len(points)
    all_points = points
    all_points_result = []
    for a in alpha:
        all_points_result.append(test_hypothesis(all_points, a))

    for i in range(len(alpha)):
        print(f"Уровень значимости alpha = {alpha[i]}")
        print(f"Объем выборки k_1 = {sample_k}")
        print(sample_result[i])
        print(f"Объем выборки k_2 = {all_points_k}")
        print(all_points_result[i])
