import numpy as np

data = np.genfromtxt('.\\iris.csv', delimiter=',')

cov_matrix = np.corrcoef(data[:, 0:2].T)
print('correlation matrix for first and second feature')
print(cov_matrix)