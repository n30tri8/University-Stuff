from scipy.optimize import linprog
import numpy as np

# zero = np.zeros(shape=5)
zero = [0, 0, 0, 0, 0]

A = np.array([[3, -5, 10, -7, 3],
                 [5, -1, 1, -6, 2]], dtype=np.float64)
# A = [[3, -5, 10, -7, 3],
#                  [5, -1, 1, -6, 2]]
b = np.array([2,
              10], dtype=np.float64)
# b = [2,
#               10]

solution = linprog(zero, A_ub=A, b_ub=b)

if solution.success:
    print(solution.x)
    print(type(solution.x))

