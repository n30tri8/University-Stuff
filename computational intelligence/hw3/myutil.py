from matplotlib import pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


def read_from_file():
    """
    read data points from csv
    :return: array of data
    """
    f = open('./data.csv')
    f.readline()
    x0 = []
    y0 = []
    x1 = []
    y1 = []
    for line in f.readlines():
        t = line.split(',')
        point_class = int(t[2])
        if  point_class == 0:
            x0.append(float(t[0]))
            y0.append(float(t[1]))
        elif point_class == 1:
            x1.append(float(t[0]))
            y1.append(float(t[1]))

    f.close()
    return x0, y0, x1, y1


def plot_dataset(x0, y0, x1, y1, graph_name):
    fig, ax = plt.subplots()

    plt.plot(x0, y0, 'bx')
    plt.plot(x1, y1, 'ro')

    plt.title('dataset')
    plt.legend(loc='upper left')
    plt.grid()

    plt.savefig(graph_name)
    # plt.show()
    plt.close()


def split_dataset(x0, y0, x1, y1):
    data = [[t0, t1] for t0, t1 in zip(x0, y0)] + [[t0, t1] for t0, t1 in zip(x1, y1)]
    class_labels = [0 for t in x0] + [1 for t in x1]

    X_train, X_test, y_train, y_test = train_test_split(data, class_labels, shuffle=True, test_size=0.2)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    x0, y0, x1, y1 = read_from_file()
    plot_dataset(x0, y0, x1, y1, './q1.png')

    X_train, X_test, y_train, y_test = split_dataset(x0, y0, x1, y1)
