from matplotlib import pyplot as plt
import numpy as np
from math import sqrt, atan, cos, sin
import file_handler

def calc_projection(gradient, points):
    inclination = atan(gradient)
    # projected_x = [( sqrt(p) if p>=0 else -1*sqrt(-p) )/sqrt(1+gradient**2) for p in points]
    # projected_y = [gradient*p for p in projected_x]
    projected_x = [p*cos(inclination) for p in points]
    projected_y = [p*sin(inclination) for p in points]

    return projected_x, projected_y

def plot(vect_x, vect_y):
    """
    Plot data points with the best vector for dimension reduction
    :return:
    """
    d1 = file_handler.read_from_file_d1()
    ds_x = [p[0] for p in d1]
    ds_y = [p[1] for p in d1]

    fig, ax = plt.subplots()

    plt.plot(ds_x, ds_y, 'bx')

    m =  vect_y / vect_x
    pca_x = np.linspace(-5,55,100)
    pca_y = m*pca_x
    plt.plot(pca_x, pca_y, '-r', label='y='+str(m)+' * x')

    z_arr = []
    for p in d1:
        z_arr.append((vect_x*p[0]) + (vect_y*p[1]))
    p_x, p_y = calc_projection(m, z_arr)
    plt.plot(p_x, p_y, 'go')

    plt.title('PCA')
    plt.legend(loc='upper left')
    plt.grid()

    file_handler.save_plot(plt, 'dataset1_pca')
    plt.show()

if __name__ == "__main__":
    plot(0.74733, 0.6644530616228659)

    