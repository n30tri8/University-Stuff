import numpy as np

data = np.genfromtxt('.\\iris.csv', delimiter=',')

cov_matrix = np.cov(data[:, 0:2].T)
print('covariance matrix for first and second feature')
print(cov_matrix)