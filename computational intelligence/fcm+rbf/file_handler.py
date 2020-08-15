import numpy as np
def read_from_file():
    """
    read data points from csv
    :return: array of data
    """
    f = open('./2clstrain1200.csv')
    xpts = []
    ypts = []
    labels = []
    for line in f.readlines():
        t = line.split(',')
        xpts.append(float(t[0]))
        ypts.append(float(t[1]))
        labels.append(int(t[2][:-1]))
        
    xpts = np.array(xpts)
    ypts = np.array(ypts)
    labels = np.array(labels, dtype=int)

    f.close()
    return xpts, ypts, labels