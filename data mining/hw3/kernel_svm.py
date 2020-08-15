import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

out_file = open('.\\outputs\\q2\\2cd_kernel_svm_results.txt', 'w')

input_data = np.genfromtxt('.\\input\\svmdata2.csv', delimiter=',')
X = input_data[:, 0:-1]
y = input_data[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

plt.figure(1)
plt.subplot(1, 1, 1).set_title('training data')
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=5, cmap=plt.cm.Paired)
plt.show()
plt.close(1)

linear_clf = svm.SVC(kernel='linear', C=0.1)
linear_clf.fit(X_train, y_train)

y_pred = linear_clf.predict(X_test)

report = classification_report(y_test, y_pred, output_dict=True)
linear_error = 1.0 - report['macro avg']['precision']
out_file.write('model error on test data; linear svm: ')
out_file.write(str(linear_error) + '\n')

plt.figure(2)
plt.subplot(1, 1, 1).set_title('test data with linear svm')
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=5, cmap=plt.cm.Paired)

ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

xx = np.linspace(xlim[0], xlim[1], 200)
yy = np.linspace(ylim[0], ylim[1], 200)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = linear_clf.decision_function(xy).reshape(XX.shape)
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
ax.scatter(linear_clf.support_vectors_[:, 0], linear_clf.support_vectors_[:, 1], s=100, linewidth=1, facecolors='none')

plt.show()
plt.close(2)
# -------------------------------------------
kernel_clf = svm.SVC(kernel='rbf')
kernel_clf.fit(X_train, y_train)

y_pred = kernel_clf.predict(X_test)

report = classification_report(y_test, y_pred, output_dict=True)
kernel_error = 1.0 - report['macro avg']['precision']
out_file.write('model error on test data; kernel svm: ')
out_file.write(str(kernel_error) + '\n')

plt.figure(3)
plt.subplot(1, 1, 1).set_title('test data with rbf svm')
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=5, cmap=plt.cm.Paired)

ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

xx = np.linspace(xlim[0], xlim[1], 200)
yy = np.linspace(ylim[0], ylim[1], 200)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = kernel_clf.decision_function(xy).reshape(XX.shape)
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
ax.scatter(kernel_clf.support_vectors_[:, 0], kernel_clf.support_vectors_[:, 1], s=100, linewidth=1, facecolors='none')

plt.show()
plt.close(3)

