import random
import typing

import numpy as np


def uniform_distribution():
    return np.random.uniform(5, 8)


def gauss_distribution():
    return random.gauss(6, 1)


def uniform_distribution_7_8():
    return np.random.uniform(7, 8)


def gauss_distribution_12_2():
    return random.gauss(12, 2)

def get_imitation_modeling_result(
        num_shifts: int,
        service_time_distribution: typing.Callable[[], float],
        interarrival_time_distribution: typing.Callable[[], float]
):
    masters_num = 5
    total_clients = 0
    total_service_time = 0

    for _ in range(num_shifts):
        time_elapsed = 0
        clients_served = 0

        while time_elapsed < 480:
            interarrival_time = interarrival_time_distribution()
            arrival_time = time_elapsed + interarrival_time
            service_time = service_time_distribution()

            time_elapsed = arrival_time
            clients_served += 1
            total_service_time += service_time

            time_elapsed += service_time

        total_clients += clients_served

    average_service_time = total_service_time / total_clients / masters_num

    return average_service_time


if __name__ == '__main__':
    shifts_counts = [1, 3, 10]
    distributions = [
        {
            'title': 'Имитационное моделирование только с распределением Гаусса',
            'service': gauss_distribution,
            'interarrival': gauss_distribution
        },
        {
            'title': 'Имитационное моделирование только с дискретным равномерным распределением',
            'service': uniform_distribution,
            'interarrival': uniform_distribution
        },
        {
            'title': 'Имитационное моделирование с дискретным равномерным распределением времени обслуживания и распределением Гаусса для времени ожидания',
            'service': uniform_distribution,
            'interarrival': gauss_distribution
        },
        {
            'title': 'Имитационное моделирование с распределением Гаусса для времени обслуживания и дискретным равномерным распределением времени ожидания',
            'service': gauss_distribution,
            'interarrival': uniform_distribution
        },
        {
            'title': 'Имитационное моделирование только с дискретным равномерным распределением в диапазоне 7-8',
            'service': uniform_distribution_7_8,
            'interarrival': uniform_distribution_7_8
        },
        {
            'title': 'Имитационное моделирование только с распределением Гаусса с матожиданием 12 и СКО 2',
            'service': gauss_distribution_12_2,
            'interarrival': gauss_distribution_12_2
        }
    ]

    for distribution in distributions:
        print(f"{distribution['title']}:")
        for shifts_count in shifts_counts:
            result = get_imitation_modeling_result(
                num_shifts=shifts_count,
                service_time_distribution=distribution['service'],
                interarrival_time_distribution=distribution['interarrival']
            )
            print(f'Результат среднего времени ожидания для количества смен '
                  f'{shifts_count}: {result:.2f} мин')
        print(' ')


