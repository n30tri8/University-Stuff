import csv
from matplotlib import pyplot
# from numpy import genfromtxt
import numpy
file = open('.\\iris.csv', 'r')

iris_csv = csv.reader(file, delimiter=',')
data = numpy.array(iris_csv)
# iris = [row for row in iris_csv]
# print(len(iris))
# print(iris[:][0])
data = numpy.genfromtxt('.\\iris.csv', delimiter=',')

fig, (axes0, axes1) = pyplot.subplots(2)
axes0.set_title('sepal length in cm')
axes0.hist(data[:, 0], 10)
axes1.set_title('petal length in cm')
axes1.hist(data[:, 2], 10)
pyplot.show()





