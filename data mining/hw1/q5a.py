import numpy

x = numpy.load('.\\data.npz')
X = numpy.zeros((len(x['x1']), 4))
X[:, 0] = numpy.ones(len(x['x1']))
X[:, 1] = x['x1']
X[:, 2] = numpy.multiply(x['x2'], x['x2'])
X[:, 3] = numpy.multiply(numpy.multiply(x['x2'], x['x2']), x['x1'])
Y = numpy.zeros((len(x['x1']), 1))
Y[:, 0] = x['y']

beta = numpy.ones((4, 1))
XBeta = numpy.zeros((len(x['x1']), 1))
Error = numpy.zeros((len(x['x1']), 1))
# computing SSE with beta in Question
beta[0] = 1
beta[1] = 3
beta[2] = 2
beta[3] = 4
# reseting beta
beta = numpy.ones((4, 1))
numpy.matmul(X, beta, XBeta)
numpy.subtract(XBeta, Y, Error)
error = numpy.linalg.norm(Error)
print('SSE error with given beta')
print(error)


alpha = 1e-5
temp = numpy.ones((4, 1))
XTX = numpy.zeros((4, 4))
XTY = numpy.zeros((4, 1))
numpy.matmul(X.T, X, XTX)
numpy.matmul(X.T, Y, XTY)
XTY = XTY*-1

decent = numpy.zeros((4, 1))

for i in range(1000000):
    numpy.matmul(XTX, beta, temp)
    numpy.add(temp, XTY, decent)
    decent = decent / numpy.linalg.norm(decent)
    step = alpha*decent
    numpy.subtract(beta, step, beta)


numpy.matmul(X, beta, XBeta)
numpy.subtract(XBeta, Y, Error)
error = numpy.linalg.norm(Error)
print('SSE error with calculated beta')
print(error)
print('calculated beta')
print(beta)

# assessing model on test data
X_test = numpy.zeros((len(x['x1_test']), 4))
X_test[:, 0] = numpy.ones(len(x['x1_test']))
X_test[:, 1] = x['x1_test']
X_test[:, 2] = numpy.multiply(x['x2_test'], x['x2_test'])
X_test[:, 3] = numpy.multiply(numpy.multiply(x['x2_test'], x['x2_test']), x['x1_test'])
Y_test = numpy.zeros((len(x['x1_test']), 1))
Y_test[:, 0] = x['y_test']

y_estimated = numpy.zeros((len(x['x1_test']), 1))
Error = numpy.zeros((len(x['x1_test']), 1))
numpy.matmul(X_test, beta, y_estimated)
numpy.subtract(y_estimated, Y_test, Error)
error = numpy.linalg.norm(Error)
print('SSE error on test data')
print(error)

# plotting y_test and Y_estimated
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x['x1_test'], x['x2_test'], Y_test, marker='x', c='r')
ax.scatter(x['x1_test'], x['x2_test'], y_estimated, marker='o', c='b')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('y_estimated(blue) and y_test(red)')
pyplot.show()

