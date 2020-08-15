import numpy as np
from scipy.optimize import line_search, linprog
from sympy import symbols, Matrix
from sympy.solvers.solveset import linsolve
import random


def newton_method(_x, _t):
    x_new = _x
    _iterations = 0
    while True:
        _iterations += 1
        dx = solve_system(hess_f(x_new, _t), -del_f_x_t(x_new, _t))
        dx = dx / np.linalg.norm(dx)
        newton_decrement = compute_newton_decrement(x_new, dx, _t)
        # if np.power(newton_decrement, 2) / 2 <= newton_tolerance:
        if newton_decrement / 2 <= newton_tolerance:
            break
        # line_search_output = line_search(f=f_x(_t), myfprime=del_f_x(_t), xk=x_new, pk=dx)
        # alpha = line_search_output[0]
        alpha = None
        if alpha is None:
            alpha = 0.01
        x_new += alpha * dx
        if _iterations % 100 == 0:
            print(_iterations)
            print(newton_decrement / 2)
    return x_new, _iterations


newton_tolerance = 0.01
t = 1
u = 20
e = 0.01
machine_eps = np.finfo(float).eps


def solve_system(_A, _b):
    syms = symbols('x:' + str(_A.shape[1]))

    system = Matrix(_A), Matrix(_b)
    solution = linsolve(system, syms)

    replacement = list()
    for variable in syms:
        if variable in solution.args[0]:
            substitution = (variable, random.uniform(-100, 100))
            replacement.append(substitution)

    return np.array(solution.args[0].subs(replacement)).astype(np.float64)


def build_vars(_m, _n):
    build = False
    _P, _A, _q, _b, _x = None, None, None, None, None
    while not build:
        _P = 200 * np.random.rand(_n, _n) - 100
        # to be sure _P is positive semi definite
        _P = np.matmul(_P, _P.T)
        _A = 200 * np.random.rand(_m, _n) - 100
        _q = 200 * np.random.rand(_n) - 100
        _b = 200 * np.random.rand(_m) - 100
        # find first feasible x
        zero = np.zeros(_n)
        solution = linprog(zero, A_ub=_A, b_ub=_b)
        build = solution.success
        _x = solution.x
    return _P, _A, _q, _b, _x


def objective_function(_x):
    output = np.matmul(_x.T, P)
    output = np.matmul(output, _x)
    output /= 2
    output += np.matmul(q.T, _x)
    return output


def del_objective_function(_x):
    output = np.matmul(_x.T, P)
    output += q
    return output


def log_barrier(_x):
    output = b - np.matmul(A, _x)
    output = np.log(output)
    output = output.sum()
    return output


def f_x_t(_x, _t):
    output = objective_function(_x) * _t
    output -= log_barrier(_x)
    return output


def f_x(_t):
    def callable_fun(_x):
        output = objective_function(_x) * _t
        output -= log_barrier(_x)
        return output

    return callable_fun


def del_f_x_t(_x, _t):
    output = del_objective_function(_x) * _t
    temp = b - np.matmul(A, _x)
    temp += machine_eps
    temp = 1.0 / temp
    temp = np.matmul(A.T, temp)
    # temp = (A.T / temp).T
    # temp = np.sum(temp, axis=1)
    output += temp
    return output


def del_f_x(_t):
    def callable_fun(_x):
        output = del_objective_function(_x) * _t
        temp = b - np.matmul(A, _x)
        temp += machine_eps
        temp = 1.0 / temp
        temp = np.matmul(A.T, temp)
        output += temp
        return output

    return callable_fun


def hess_f(_x, _t):
    output = _t * P
    temp = b - np.matmul(A, _x)
    temp += machine_eps
    temp = 1.0 / temp
    temp = np.diag(temp)
    np.power(temp, 2, out=temp)
    # temp = np.power(b - np.matmul(A, _x), 2)
    # temp2 = np.ndarray(b.shape, np.float64)
    # for _i in range(temp2.shape[0]):
    #     temp2[_i] = np.matmul(A[_i], A[_i].T)
    # temp = (temp2.T / temp).T
    temp = np.matmul(A.T, temp)
    temp = np.matmul(temp, A)
    output += temp
    if not is_pos_def(output):
        print('not output')
    return output


def compute_newton_decrement(_x, _dx, _t):
    dec = np.matmul(_dx.T, hess_f(_x, _t))
    dec = np.matmul(dec, _dx)
    # dec = np.sqrt(dec)
    return dec


def is_pos_def(_x):
    return np.all(np.linalg.eigvals(_x) > 0)


# main
m = 3
n = 8
# 100*50
P, A, q, b, x = build_vars(m, n)
duality_gap_seq = list()

while m / t > e:
    x, iterations = newton_method(x, t)
    # update stat
    duality_gap = m / t
    for i in range(iterations):
        duality_gap_seq.append(m / t)

    t = t * u
    print('t, iter, gap' + str(t) + '  ' + str(iterations) + '   ' + str(duality_gap))
duality_gap_seq.append(m / t)

print(duality_gap_seq)
