import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier

out_file = open('.\\outputs\\q3\\ann_sklearn.txt', 'w')

input_data = np.genfromtxt('.\\input\\Drinks.csv', delimiter=',')
X = input_data[:, 0:-3]
y = input_data[:, -3:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

clf = MLPClassifier(hidden_layer_sizes=(8, 5), activation='tanh', solver='sgd', alpha=1e-5, random_state=1,
                    learning_rate='constant', learning_rate_init=0.7)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

report = classification_report(y_test, y_pred, output_dict=True)

out_file.write('class 0 precision: ' + str(report['0']['precision']) + '\n')
out_file.write('class 1 precision: ' + str(report['1']['precision']) + '\n')
out_file.write('class 2 precision: ' + str(report['2']['precision']) + '\n')
out_file.write('macro avg. precision: ' + str(report['macro avg']['precision']) + '\n')
out_file.write('loss: ' + str(clf.loss_) + '\n')
out_file.write('no. iterations: ' + str(clf.n_iter_) + '\n')
out_file.write('----------------' + '\n')

i = 1
for layer in clf.coefs_:
    out_file.write('weight matrix for layer ' + str(i) + '\n')
    out_file.write(str(layer))
    out_file.write('\n')
    i += 1
i = 2
for layer in clf.intercepts_:
    out_file.write('bias vector for layer ' + str(i) + '\n')
    out_file.write(str(layer))
    out_file.write('\n')
    i += 1

