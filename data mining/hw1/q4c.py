from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

data = np.genfromtxt('.\\iris.csv', delimiter=',')


fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[0:49, 0], data[0:49, 1], 1, marker='x', c='r')
ax.scatter(data[50:99, 0], data[50:99, 1], 1, marker='*', c='b')
ax.scatter(data[100:149, 0], data[100:149, 1], 1, marker='o', c='g')
ax.set_xlabel('sepal length in cm')
ax.set_ylabel('sepal width in cm')
ax.set_zlabel('specie')
ax.set_title('Setosa(red)  Versicolour(blue)   Virginica(green)')
pyplot.show()