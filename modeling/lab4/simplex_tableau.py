from docplex.mp.model import Model

m = Model()
x_1 = m.continuous_var(name='x_1', lb=0)
x_2 = m.continuous_var(name='x_2', lb=0)
x_3 = m.continuous_var(name='x_3', lb=0)
x_4 = m.continuous_var(name='x_4', lb=0)
x_5 = m.continuous_var(name='x_5', lb=0)

m.add_constraint(2 * x_1 + 5 * x_2 - x_3 == 19)
m.add_constraint(5 * x_1 + 2 * x_2 - x_4 == 21)
m.add_constraint(3 * x_1 + 4 * x_2 >= 0)
#m.add_constraint(-16/21 * x_3 - 2/21 * x_4 + x_5 == 11/21)


m.minimize(3 * x_1 + 4 * x_2)

c = m.get_cplex()
c.parameters.simplex.limits.iterations.set(100)
c.parameters.lpmethod.set(c.parameters.lpmethod.values.primal)
# this while loop will print the tableau after each
# simplex iteration
while c.solution.get_status() != c.solution.status.optimal:
    c.solve()
    print("=== Симплекс-таблица ===")
    for tableau_row in c.solution.advanced.binvarow():
        print(tableau_row)

m.solve()
print("\n=== Решение ===")
m.print_solution()
