from sympy import symbols, Matrix, Symbol
from sympy.solvers.solveset import linsolve
import numpy as np
import random
from sympy import MatrixSymbol, MatrixExpr, MatMul, Identity
from sympy.solvers.inequalities import solve_rational_inequalities
from sympy.solvers import solveset
from sympy import S, solve

# syms = symbols('x:5')
# A = np.array([[3, -5, 10, -7, 3],
#               [5, -1, 1, -6, 2]], dtype=np.float64)
# b = np.array([2,
#               10], dtype=np.float64)
#
# system = Matrix(A), Matrix(b)
# solution = linsolve(system, syms)
#
# replacement = list()
# for variable in syms:
#     if variable in solution.args[0]:
#         substitution = (variable, random.uniform(-1000, 1000))
#         replacement.append(substitution)
# # print(solution.args[0].subs(replacement))
# # print(type(solution.args[0].subs(replacement)[0]))
#
# x_sol = np.array(solution.args[0].subs(replacement)).astype(np.float64)
#
# print(np.matmul(A, x_sol))
# print(b)

# -----------------------------

# x = MatrixSymbol('x', 5, 1)
# A = np.array([[3, -5, 10, -7, 3],
#               [5, -1, 1, -6, 2]], dtype=np.float64)
# b = np.array([2, 10], dtype=np.float64)
#
# inequality = MatMul(Matrix(A), x) < Matrix(b)
# print(inequality)
# solution = linsolve(inequality, x)

# replacement = list()
# for variable in syms:
#     if variable in solution.args[0]:
#         substitution = (variable, random.uniform(-1000, 1000))
#         replacement.append(substitution)
# print(solution.args[0].subs(replacement))
# print(type(solution.args[0].subs(replacement)[0]))

# x_sol = np.array(solution.args[0].subs(replacement)).astype(np.float64)
#
# print(np.matmul(A, x_sol))
# print(b)

# -----------------------------------------
# x = MatrixSymbol('x', 5, 1)
# A = np.array([[3, -5, 10, -7, 3],
#               [5, -1, 1, -6, 2]], dtype=np.float64)
# b = np.array([2,
#               10], dtype=np.float64)
#
# _a = Matrix(A[0, :])
# inequality0 = MatMul(_a.T, x) < b[0]*Identity(1)
# print(inequality0)
# solution = linsolve(inequality, x)

# replacement = list()
# for variable in syms:
#     if variable in solution.args[0]:
#         substitution = (variable, random.uniform(-1000, 1000))
#         replacement.append(substitution)
# print(solution.args[0].subs(replacement))
# print(type(solution.args[0].subs(replacement)[0]))

# x_sol = np.array(solution.args[0].subs(replacement)).astype(np.float64)
#
# print(np.matmul(A, x_sol))
# print(b)

# x = Symbol('x')
# y = Symbol('y')
# inequ = [3*x - 2*y < 5, -10*x + 4*y > -6]
# inequ2 = (x , -1, '>')
# print(type(inequ))
# solution = solveset(f=[[inequ, inequ2]], symbol=x, domain=S.Reals)
# solution = solve_rational_inequalities([inequ, inequ2])
# solution = solve(inequ, [x, y])
# print(solution)
