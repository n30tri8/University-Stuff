def read_from_file_d1():
    """
    read data points from csv
    :return: array of data
    """
    f = open('./Dataset/Dataset1.csv')
    f.readline()
    out_arr = []
    for line in f.readlines():
        t = line.split(',')
        out_arr.append((float(t[0]), float(t[1])))

    return out_arr

def read_from_file_d2():
    """
    read data points from csv
    :return: array of data
    """
    f = open('./Dataset/Dataset2.csv')
    f.readline()
    out_arr = []
    for line in f.readlines():
        t = line.split(',')
        out_arr.append((float(t[0]), float(t[1])))

    return out_arr

def save_plot(plt, name):
    plt.savefig('./' + name + '.png')