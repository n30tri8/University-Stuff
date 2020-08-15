import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def build_model(X, hidden_nodes, output_dim=3):
    model = {}
    input_dim = X.shape[1]
    model['W1'] = np.random.randn(input_dim, hidden_nodes[0]) / np.sqrt(input_dim)
    model['b1'] = np.zeros((1, hidden_nodes[0]))
    model['W2'] = np.random.randn(hidden_nodes[0], hidden_nodes[1]) / np.sqrt(hidden_nodes[0])
    model['b2'] = np.zeros((1, hidden_nodes[1]))
    model['W3'] = np.random.randn(hidden_nodes[1], output_dim) / np.sqrt(hidden_nodes[1])
    model['b3'] = np.zeros((1, output_dim))
    return model


def feed_forward(model, x):
    W1, b1, W2, b2, W3, b3 = model['W1'], model['b1'], model['W2'], model['b2'], model['W3'], model['b3']
    # Forward propagation
    z1 = x.dot(W1) + b1
    a1 = np.tanh(z1)

    z2 = a1.dot(W2) + b2
    a2 = np.tanh(z2)

    z3 = a2.dot(W3) + b3
    # soft max
    exp_scores = np.exp(z3)
    out = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

    return z1, a1, z2, a2, z3, out


# def calculate_loss(model,X,y,reg_lambda):
#     num_examples = X.shape[0]
#     W1, b1, W2, b2, W3, b3 = model['W1'], model['b1'], model['W2'], model['b2'], model['W3'], model['b3']
#     # Forward propagation to calculate our predictions
#     z1, a1, z2, a2, z3, out = feed_forward(model, X)
#     probs = out / np.sum(out, axis=1, keepdims=True)
#     # Calculating the loss
#     corect_logprobs = -np.log(probs[:, y])
#     loss = np.sum(corect_logprobs)
#     # Add regulatization term to loss (optional)
#     loss += reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)) + np.sum(np.square(W3)))
#     return 1./num_examples * loss


def calculate_loss(model,X,y,reg_lambda):
    # Forward propagation to calculate our predictions
    z1, a1, z2, a2, z3, out = feed_forward(model, X)
    se = np.linalg.norm(out - y, axis=1, keepdims=True)
    sse = se.sum(axis=0, keepdims=True)
    return sse


def backprop(X,y,model,z1,a1,z2,a2,z3,output,reg_lambda):
    delta3 = output - y # yhat - y0
    dW3 = (a2.T).dot(delta3)
    db3 = np.sum(delta3, axis=0, keepdims=True)
    delta2 = delta3.dot(model['W3'].T) * (1 - np.power(a2, 2))
    dW2 = np.dot(a1.T, delta2)
    db2 = np.sum(delta2, axis=0)
    delta1 = delta2.dot(model['W2'].T) * (1 - np.power(a1, 2))
    dW1 = np.dot(X.T, delta1)
    db1 = np.sum(delta1, axis=0)
    # Add regularization terms
    dW3 += reg_lambda * model['W3']
    dW2 += reg_lambda * model['W2']
    dW1 += reg_lambda * model['W1']
    return dW1, dW2, dW3, db1, db2, db3


def train(model, X, y, num_passes=10000, reg_lambda=0.1, learning_rate=0.1):
    done = False
    i = 0
    losses = []
    while not done:
        #feed forward
        z1,a1,z2,a2,z3,output = feed_forward(model, X)
        #backpropagation
        dW1, dW2, dW3, db1, db2, db3 = backprop(X,y,model,z1,a1,z2,a2,z3,output,reg_lambda)
        #update weights and biases
        # TODO should i linalg.norm dX?
        model['W1'] -= learning_rate * dW1
        model['b1'] -= learning_rate * db1
        model['W2'] -= learning_rate * dW2
        model['b2'] -= learning_rate * db2
        model['W3'] -= learning_rate * dW3
        model['b3'] -= learning_rate * db3
        if i % 100 == 0:
            loss = calculate_loss(model, X, y, reg_lambda)
            losses.append(loss)
            print("Loss after iteration %i: %f" % (i, loss))
            if loss < 0.1:
                done = True
        i += 1
    return model, losses, i


# main
out_file = open('.\\outputs\\q3\\ann_sklearn.txt', 'w')

input_data = np.genfromtxt('.\\input\\Drinks.csv', delimiter=',')
X = input_data[:, 0:-3]
y = input_data[:, -3:]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

num_examples = len(X_train) # training set size
nn_input_dim = 13 # input layer dimensionality
nn_output_dim = 3 # output layer dimensionality
hidden_layers_dim = [8, 5]
learning_rate = 0.07 # learning rate for gradient descent
reg_lambda = 0.01 # regularization strength
model = build_model(X_train, hidden_layers_dim, nn_output_dim)

model, losses, no_iters = train(model, X_train, y_train, reg_lambda=reg_lambda, learning_rate=learning_rate)

z1,a1,z2,a2,z3, y_pred = feed_forward(model, X_test)
# fix y_pred
for i in range(y_pred.shape[0]):
    for j in range(y_pred.shape[1]):
        if y_pred[i, j] >= 0.5:
            y_pred[i, j] = 1
        else:
            y_pred[i, j] = 0
# print(y_pred)

report = classification_report(y_test, y_pred, output_dict=True)

out_file = open('.\\outputs\\q3\\ann_4layer.txt', 'w')

out_file.write('class 0 precision: ' + str(report['0']['precision']) + '\n')
out_file.write('class 1 precision: ' + str(report['1']['precision']) + '\n')
out_file.write('class 2 precision: ' + str(report['2']['precision']) + '\n')
out_file.write('macro avg. precision: ' + str(report['macro avg']['precision']) + '\n')
out_file.write('loss: ' + str(losses[-1]) + '\n')
out_file.write('no. iterations: ' + str(no_iters) + '\n')
out_file.write('----------------' + '\n')

for i in range(1, 4):
    out_file.write('weight matrix for layer ' + str(i) + '\n')
    ref = 'W' + str(i)
    out_file.write(str(model[ref]))
    out_file.write('\n')

for i in range(1, 4):
    out_file.write('bias vector for layer ' + str(i+1) + '\n')
    ref = 'b' + str(i)
    out_file.write(str(model[ref]))
    out_file.write('\n')
    i += 1
