import myutil
from math import exp
import random


def Sigmoid(x):
    return 1/(1 + exp(-x))


def compute_y(W, X):
    t = W[0] * X[0] + W[1] * X[1] + W[2]
    return Sigmoid(t)


def compute_network_cost(W, X_train, y_train):
    total_cost = 0
    for X_, y_ in zip(X_train, y_train):
        y_net = compute_y(W, X_)
        total_cost += ((y_net - y_)**2)/2
    return total_cost


def grad_W(W, X_train, y_train):
    _grad_W = [0 for i in W]
    for X_, y_ in zip(X_train, y_train):
        y_net = compute_y(W, X_)
        _grad_W[0] += (y_net - y_) * y_net * (1 - y_net) * X_[0]
        _grad_W[1] += (y_net - y_) * y_net * (1 - y_net) * X_[1]
        _grad_W[2] += (y_net - y_) * y_net * (1 - y_net)
    
    _grad_W_length = sum([v**2 for v in _grad_W]) ** 0.5
    if _grad_W_length != 0:
        _grad_W = [(v / _grad_W_length) for v in _grad_W]
    return _grad_W
    

def test_model(W, X_test, y_test, graph_name):
    mispredictions = 0
    x0 = []
    y0 = []
    x1 = []
    y1 = []
    for X_, y_ in zip(X_test, y_test):
        y_net = compute_y(W, X_)
        # convert y_net to class label
        if y_net >= 0.5:
            y_net = 1.0
        else:
            y_net = 0.0
        # divide test data to class 0 and 1
        if y_net == 0.0:
            x0.append(X_[0])
            y0.append(X_[1])
        elif y_net == 1.0:
            x1.append(X_[0])
            y1.append(X_[1])
        # compare predicted class to actual class
        if y_net != y_:
             mispredictions += 1

    total = len(y_test)
    percent = (total - mispredictions)/total
    myutil.plot_dataset(x0, y0, x1, y1, graph_name)
    return percent


if __name__ == "__main__":
    
    x0, y0, x1, y1 = myutil.read_from_file()
    X_train, X_test, y_train, y_test = myutil.split_dataset(x0, y0, x1, y1)

    W = random.sample(range(-5, 5), 3)
    n_epoch = 10000
    lr = 0.01

    for i in range(n_epoch):
        dW = grad_W(W, X_train, y_train)
        # add pace to weights and biases
        W = [(w - lr*dw) for w, dw in zip(W, dW)]

        if i%100 == 0:
            total_cost = compute_network_cost(W, X_train, y_train)
            print('network cost in epoch %d: %f'%(i, total_cost))

    accuracy = test_model(W, X_test, y_test, './one_layer_test_model.png')
    print('W = %s'%str(W))
    print('model accuracy: %f'%accuracy)
    
    
