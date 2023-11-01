from scipy.optimize import linprog

obj = [3, 4]

lhs_ineq = [
    [-2, -5],
    [-5, -2]
]

rhs_ineq = [-19, -21]
bounds = [
    (0, float("inf")),
    (0, float("inf"))
]

opt = linprog(
    c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, bounds=bounds, method='highs-ds'
)

z = opt.fun
x_1, x_2 = opt.x
x_3 = rhs_ineq[0] - lhs_ineq[0][0] * x_1 - lhs_ineq[0][1] * x_2
x_4 = rhs_ineq[1] - lhs_ineq[1][0] * x_1 - lhs_ineq[1][1] * x_2

print('Решение, полученное двойственным симплекс-методом:')
print(f'\t{z=:.2f}')
print(f'\t{x_1=:.2f}')
print(f'\t{x_2=:.2f}')
print(f'\t{x_3=:.2f}')
print(f'\t{x_4=:.2f}')
