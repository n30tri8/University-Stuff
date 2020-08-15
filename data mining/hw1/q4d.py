from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('.\\iris.csv', delimiter=',')
mean = np.mean(data, axis=0)
var = np.var(data, axis=0)

print('mean:')
print(mean)
print('var:')
print(var)