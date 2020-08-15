import numpy as np

data = np.genfromtxt('.\\iris.csv', delimiter=',')

mean = np.zeros((3, 4))
for i in range(3):
    for j in range(4):
        mean[i, j] = np.mean(data[i*50:i*50+49, j], axis=0)
print('mean value for specie/feature')
print(mean)

var = np.zeros((3, 4))
for i in range(3):
    for j in range(4):
        var[i, j] = np.var(data[i*50:i*50+49, j], axis=0)
print('variance for specie/feature')
print(var)

