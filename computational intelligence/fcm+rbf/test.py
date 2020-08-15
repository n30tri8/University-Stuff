from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']

# # Define three cluster centers
# centers = [[4, 2],
#            [1, 7],
#            [5, 6]]

# # Define three cluster sigmas in x and y, respectively
# sigmas = [[0.8, 0.3],
#           [0.3, 0.5],
#           [1.1, 0.7]]

# # Generate test data
# np.random.seed(42)  # Set seed for reproducibility
# xpts = []
# ypts = []
# labels = []
# for i, ((xmu, ymu), (xsigma, ysigma)) in enumerate(zip(centers, sigmas)):
#     xpts = np.hstack((xpts, np.random.standard_normal(3) * xsigma + xmu))
#     ypts = np.hstack((ypts, np.random.standard_normal(3) * ysigma + ymu))
#     labels = np.hstack((labels, np.ones(3) * i))



# # Visualize the test data
# fig0, ax0 = plt.subplots()
# for label in range(3):
#     ax0.plot(xpts[labels == label], ypts[labels == label], '.',
#              color=colors[label])
# ax0.set_title('Test data: 200 points x3 clusters.')

# # plt.show()

# alldata = np.vstack((xpts, ypts))

# cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata, 3, 2, error=0.005, maxiter=1000, init=None)
# cluster_membership = np.argmax(u, axis=0)

# print(u)
# print(cluster_membership)
cluster_range = np.arange(2, 40, 1)
lambda_range = np.arange(0.1, 3, 0.2)
accuracy_dict = {}

for c in cluster_range:
    for l in lambda_range:
        accuracy_dict[str(c) + '+' + f"{l:.1f}"] = (c, l)

X = cluster_range
Y = lambda_range
X, Y = np.meshgrid(X, Y)
print(X)
print(Y)
Z = np.ndarray(X.shape)
for idx0 in range(X.shape[0]):
    for idx1 in range(X.shape[1]):
        X_val = str(X[idx0, idx1])
        Y_val = f"{Y[idx0, idx1]:.1f}"
        try:
            Z[idx0, idx1] = accuracy_dict[X_val+'+'+Y_val][0]
        except KeyError:
            print('error')
            print('no_clusters: ' + X_val)
            print('lambda' + Y_val)

if str(no_cluster) + '+' + f"{lambda_rad:.1f}" == '23+2.9':
                print('put 23+2.9')
                zjzzj = accuracy_dict['23+2.9']
