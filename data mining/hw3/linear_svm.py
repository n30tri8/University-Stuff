import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

out_file = open('.\\outputs\\q2\\1c_linear_svm_results.txt', 'w')

input_data = np.genfromtxt('.\\input\\svmdata.csv', delimiter=',')
X = input_data[:, 0:-1]
y = input_data[:, -1]

X_train_validation, X_test, y_train_validation, y_test = train_test_split(X, y, test_size=0.20)
X_train, X_validation, y_train, y_validation = train_test_split(X_train_validation, y_train_validation, test_size=0.20)

plt.figure(1)
plt.subplot(1, 1, 1).set_title('training data')
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=5, cmap=plt.cm.Paired)
plt.show()
plt.close(1)

C_param = [0.001, 0.01, 1, 10, 1000]
validation_error = list()
clf_list = list()

for penalty in C_param:
    clf = svm.SVC(kernel='linear', C=penalty)
    clf.fit(X_train, y_train)
    clf_list.append(clf)

    y_pred = clf.predict(X_validation)

    report = classification_report(y_validation, y_pred, output_dict=True)
    error = 1.0 - report['macro avg']['precision']
    validation_error.append(error)

plt.figure(2)
plt.subplot(1, 1, 1).set_title('validation error per model')
plt.semilogx(C_param, validation_error)
plt.xlabel('C param')
plt.ylabel('1 - precision')
plt.show()
plt.close(2)

clf = clf_list[np.argmin(validation_error)]

y_pred = clf.predict(X_test)

report = classification_report(y_test, y_pred, output_dict=True)
error = 1.0 - report['macro avg']['precision']
out_file.write('model error on test data: ')
out_file.write(str(error) + '\n')

plt.figure(3)
plt.subplot(1, 1, 1).set_title('test data + svm line')
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=5, cmap=plt.cm.Paired)

# plot the decision function
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
# plot support vectors
ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100, linewidth=1, facecolors='none', edgecolors='k')

plt.show()
plt.close(3)
