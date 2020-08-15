import numpy as np

data = np.genfromtxt('.\\iris.csv', delimiter=',')

cov_matrix = np.corrcoef(data[100:149, 0:4].T)
print('correlation matrix for all features of virginia')
print(cov_matrix)

