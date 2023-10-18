import pulp

import time
start = time.time()

x_11 = pulp.LpVariable("x_11", lowBound=0)
x_12 = pulp.LpVariable("x_12", lowBound=0)
x_13 = pulp.LpVariable("x_13", lowBound=0)
z_1 = pulp.LpVariable("z_1", lowBound=143.97)

x_21 = pulp.LpVariable("x_21", lowBound=0)
x_22 = pulp.LpVariable("x_22", lowBound=0)
x_23 = pulp.LpVariable("x_23", lowBound=0)
z_2 = pulp.LpVariable("z_2", lowBound=151.17)

problem = pulp.LpProblem('0', pulp.LpMinimize)
problem += z_1 + z_2, "Функция цели"
problem += 143.97 * x_11 + 201.56 * x_12 + 215.95 * x_13 == 1500 * z_1
problem += 151.17 * x_21 + 340.45 * x_22 + 302.54 * x_23 == 1200 * z_2
problem += x_11 + x_12 + x_13 == 1500
problem += x_21 + x_22 + x_23 == 1200
problem += x_11 <= 550
problem += x_12 <= (800 - 550)
problem += x_11 + x_12 <= 800
problem += x_21 <= 620
problem += x_22 <= (900 - 620)
problem += x_21 + x_22 <= 900

problem.solve()
print("Результат:")

variables = {
    'x_11': "Обычный тип производства гаечных ключей",
    'x_12': "Тип производства гаечных ключей 'Сверхурочные'",
    'x_13': "Тип производства гаечных ключей 'Субподрядчики'",
    'x_21': "Обычный тип производства отвёрток",
    'x_22': "Тип производства отвёрток 'Сверхурочные'",
    'x_23': "Тип производства отвёрток 'Субподрядчики'",
    'z_1': "Стоимость гаечного ключа",
    'z_2': "Стоимость отвёртки"
}

values = {
    'x_11': 0,
    'x_12': 0,
    'x_13': 0,
    'x_21': 0,
    'x_22': 0,
    'x_23': 0,
    'z_1': 0,
    'z_2': 0
}

for variable in problem.variables():
    values[variable.name] = variable.varValue
    print(f"{variables[variable.name]:50} {variable.varValue:>7.2f}")
