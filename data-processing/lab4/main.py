import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


def trust_interval_with_unknown_mean(
        sample: np.array,
        q: float
) -> tuple[float, float]:

    alpha = 1 - q
    data = np.array(sample)
    n = len(sample)
    sample_variance = np.var(data, ddof=1)

    chi2_lower = stats.chi2.ppf(alpha / 2, df=n - 1)
    chi2_upper = stats.chi2.ppf(1 - alpha / 2, df=n - 1)

    lower_bound = (n - 1) * sample_variance / chi2_upper
    upper_bound = (n - 1) * sample_variance / chi2_lower

    return lower_bound, upper_bound


def trust_interval_with_known_a(
        sample: np.array,
        q: float
) -> tuple[float, float]:

    alpha = 1 - q
    sample_variance = np.var(sample, ddof=0)
    degrees_of_freedom = n = len(sample)

    chi2_lower = stats.chi2.ppf(alpha / 2, df=degrees_of_freedom)
    chi2_upper = stats.chi2.ppf(1 - alpha / 2, df=degrees_of_freedom)

    lower_bound = (n * sample_variance) / chi2_upper
    upper_bound = (n * sample_variance) / chi2_lower

    return lower_bound, upper_bound


if __name__ == '__main__':

    mean, sigma = 4, 1
    q = 0.8

    first_count = 15
    second_count = first_count * 70

    first_sample = np.random.normal(mean, sigma, first_count)
    second_sample = np.random.normal(mean, sigma, second_count)

    print('Математическое ожидание неизвестно:')

    lower_bound_SPA, upper_bound_SPA = trust_interval_with_unknown_mean(
        first_sample, q
    )
    print(
        "\tДоверительный интервал для σ^2 при малой выборке и при уровне "
        f"доверия {q}: ({lower_bound_SPA:.2f}, {upper_bound_SPA:.2f})"
    )

    lower_bound_BPA, upper_bound_BPA = trust_interval_with_unknown_mean(
        second_sample, q
    )
    print(
        "\tДоверительный интервал для σ^2 при большой выборке и при уровне "
        f"доверия {q}: ({lower_bound_BPA:.2f}, {upper_bound_BPA:.2f})"
    )

    print(f"\nМатематическое ожидание равно a_0 = {mean}:")
    lower_bound_SPB, upper_bound_SPB = trust_interval_with_known_a(
        first_sample, q
    )
    print(
        "\tДоверительный интервал для σ^2 при малой выборке и при уровне доверия "
        f"{q}: ({lower_bound_SPB:.2f}, {upper_bound_SPB:.2f})"
    )

    lower_bound_BPB, upper_bound_BPB = trust_interval_with_known_a(
        second_sample, q
    )
    print(
        "\tДоверительный интервал для σ^2 при малой выборке и при уровне доверия "
        f"{q}: ({lower_bound_BPB:.2f}, {upper_bound_BPB:.2f})"
    )

    new_q = np.linspace(0.1, 0.99, 50)
    first_y = []
    second_y = []
    third_y = []
    fourth_y = []

    for i in range(50):
        left, right = trust_interval_with_unknown_mean(first_sample, new_q[i])
        first_y.append(right - left)
        left, right = trust_interval_with_unknown_mean(second_sample, new_q[i])
        second_y.append(right - left)
        left, right = trust_interval_with_known_a(first_sample, new_q[i])
        third_y.append(right - left)
        left, right = trust_interval_with_known_a(second_sample, new_q[i])
        fourth_y.append(right - left)

    plt.figure(figsize=(8, 6))

    plt.plot(
        new_q, first_y, 'r', label='$n_1$ при неизвестном мат. ожидании'
    )
    plt.plot(
        new_q, second_y, 'g', label='$n_2$ при неизвестном мат. ожидании'
    )
    plt.plot(
        new_q, third_y, 'b', label='$n_1$ при мат. ожидании $a_0=4$'
    )
    plt.plot(
        new_q, fourth_y, 'c', label='$n_2$ при мат. ожидание $a_0=4$'
    )

    plt.ylabel('Длина доверительного интервала')
    plt.xlabel('q')
    plt.legend()
    plt.show()
