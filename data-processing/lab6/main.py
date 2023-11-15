from scipy import stats

# Данные
data = [
    27, 28, 24, 26, 27, 25, 25, 24, 24, 24, 25, 28, 22, 25, 24, 28, 27, 26,
    31, 25, 28, 27, 27, 25
]

alpha = 0.05
null_hypothesis_mean = 20
# Проводим одновыборочный t-тест
t_statistic, p_value = stats.ttest_1samp(
    data, null_hypothesis_mean, alternative='greater'
)

# Печатаем результаты
print('t-статистика:', t_statistic)
print('p-значение:', p_value)

# Проверяем уровень значимости
if p_value < alpha:
    print(
        'Отвергаем нулевую гипотезу: среднее значение разгибания запястья '
        'больше 20 градусов.'
    )
else:
    print(
        'Не отвергаем нулевую гипотезу: среднее значение разгибания запястья '
        'не превышает 20 градусов.'
    )
