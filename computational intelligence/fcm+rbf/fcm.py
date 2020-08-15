import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import file_handler
from math import exp
from sklearn.model_selection import train_test_split
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

u_exponent = 2


def fcm(data, no_cluster):
    
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(data, c=no_cluster, m=u_exponent, error=0.005, maxiter=1000, init=None)
    # cluster_membership = np.argmax(u, axis=0)

    # print(np.shape(u))
    # print(np.shape(cluster_membership))
    return cntr, u


def enumerate_classes(labels):
    class_types = []
    for l in labels:
        if l not in class_types:
            class_types.append(l)
    
    return class_types


def calc_u(test_data, cntr):
    no_cntr = len(cntr)
    no_testdata = len(test_data[0])
    _2divm_1 = 2 / (u_exponent - 1)
    distance_matrix = np.zeros(shape=(no_cntr, no_testdata))
    for x_idx in range(no_testdata):
        for c_idx in range(no_cntr):
            distance_matrix[c_idx, x_idx] = 1 / np.linalg.norm(test_data[:, x_idx] - cntr[c_idx])**_2divm_1
    
    sum_matrix = np.sum(distance_matrix, axis=0)
    u = np.zeros(shape=(no_cntr, no_testdata))
    for x_idx in range(no_testdata):
        for c_idx in range(no_cntr):
            u[c_idx, x_idx] = distance_matrix[c_idx, x_idx] / sum_matrix[x_idx]
    
    return u



if __name__ == "__main__":
    xpts, ypts, labels = file_handler.read_from_file()
    class_types = enumerate_classes(labels)
    no_class_types = len(class_types)
    alldata = np.vstack((xpts, ypts))
    X_train, X_test, y_train, y_test = train_test_split(alldata.T, labels, shuffle=True, test_size=0.3)
    train_data = X_train.T
    train_size = len(X_train)

    accuracy_dict = {}
    cluster_range = np.arange(2, 40, 1)
    lambda_range = np.arange(0.1, 3, 0.2)

    for no_cluster in cluster_range:
        no_cluster = int(no_cluster)
        cntr, u = fcm(train_data, no_cluster)
        # u = (no_cluster, train_size)
        # cntr = (no_cluster, data_shape)
        # train_data = (data_shape, train_size)
        # labels = (alldata_size,)

        for lambda_rad in lambda_range:
            # calc G
            G = np.zeros(shape=(train_size, no_cluster))
            
            for j in range(no_cluster):
                temp0 = []
                for temp_idx in range(train_size):
                    temp1 = train_data[:, temp_idx] - cntr[j]
                    temp1 = (u[j][temp_idx]**u_exponent) * np.matmul(temp1.T, temp1)
                    temp0.append(temp1)
                C = sum(temp0) / (sum([x**u_exponent for x in u[j]]))
                for i in range(train_size):
                    temp0 = train_data[:, i] - cntr[j]
                    temp1 = exp(-1 * lambda_rad * np.matmul(temp0.T, temp0) * C)
                    G[i, j] = temp1
            
            # calc W
            Y = np.zeros(shape=(train_size, no_class_types))
            for temp_idx in range(train_size):
                temp0 = y_train[temp_idx]
                Y[temp_idx, temp0] = 1

            GtG_1 = np.linalg.inv(np.matmul(G.T, G))
            GtG_1G = np.matmul(GtG_1, G.T)
            W = np.matmul(GtG_1G, Y)

            # y~
            GW = np.matmul(G, W).T
            y_pred = np.argmax(GW, axis=0)

            # accuracy
            false_pred = np.sum(np.abs(np.sign(y_train - y_pred)))
            accuracy = 1 - false_pred/train_size

            # # Visualize the train data
            # colors = ['g', 'b', 'orange', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen', 'r']
            # fig0, ax0 = plt.subplots(2, 1)
            # for label in range(no_cluster):
            #     ax0[0].plot(xpts[labels == label], ypts[labels == label], '.', color=colors[label])
            # for label in range(no_cluster):
            #     select_true_preds = []
            #     select_false_preds = []
            #     for pred, true_label in zip(y_pred, y_train):
            #         select_true_preds.append(pred == true_label and true_label == label)
            #         select_false_preds.append(pred != true_label and true_label == label)
            #     ax0[1].plot(train_data[0][select_true_preds], train_data[1][select_true_preds], '.', color=colors[label])
            #     ax0[1].plot(train_data[0][select_false_preds], train_data[1][select_false_preds], '.', color='r')

            # ax0[0].set_title('original labels')
            # ax0[1].set_title('trained model')
            # # Mark the center of each fuzzy cluster
            # for pt in cntr:
            #     ax0[1].plot(pt[0], pt[1], 'ks')

            # plt.show()

            # predict on test data:
            test_data = X_test.T
            test_size = len(X_test)
            G_testdata = np.zeros(shape=(test_size, no_cluster))
            
            u_testdata = calc_u(test_data, cntr)

            for j in range(no_cluster):
                temp0 = []
                for temp_idx in range(test_size):
                    temp1 = test_data[:, temp_idx] - cntr[j]
                    temp1 = (u_testdata[j][temp_idx]**u_exponent) * np.matmul(temp1.T, temp1)
                    temp0.append(temp1)
                C = sum(temp0) / (sum([x**u_exponent for x in u_testdata[j]]))
                for i in range(test_size):
                    temp0 = test_data[:, i] - cntr[j]
                    temp1 = exp(-1 * lambda_rad * np.matmul(temp0.T, temp0) * C)
                    G_testdata[i, j] = temp1

            # y~
            Gbar_x_W = np.matmul(G_testdata, W).T
            y_pred_test_data = np.argmax(Gbar_x_W, axis=0)

            # accuracy
            false_pred = np.sum(np.abs(np.sign(y_test - y_pred_test_data)))
            accuracy = 1 - false_pred/test_size
            # print('no_clusters=%d; lambda=%f; accuracy on test data=%f'%(no_cluster, lambda_rad, accuracy))
            accuracy_dict[str(no_cluster) + '+' + f"{lambda_rad:.1f}"] = (no_cluster, lambda_rad, accuracy)

            # # Visualize the test data
            # colors = ['g', 'b', 'orange', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen', 'r']
            # fig0, ax0 = plt.subplots(2, 1)
            # for label in range(no_cluster):
            #     ax0[0].plot(xpts[labels == label], ypts[labels == label], '.', color=colors[label])
            # for label in range(no_cluster):
            #     select_true_preds = []
            #     select_false_preds = []
            #     for pred, true_label in zip(y_pred_test_data, y_test):
            #         select_true_preds.append(pred == true_label and true_label == label)
            #         select_false_preds.append(pred != true_label and true_label == label)
            #     ax0[1].plot(test_data[0][select_true_preds], test_data[1][select_true_preds], '.', color=colors[label])
            #     ax0[1].plot(test_data[0][select_false_preds], test_data[1][select_false_preds], '.', color='r')

            # ax0[0].set_title('original labels(no_clusters=%d; lambda=%f)'%(no_cluster, lambda_rad))
            # ax0[1].set_title('model on test data(no_clusters=%d; lambda=%f)'%(no_cluster, lambda_rad))
            # # Mark the center of each fuzzy cluster
            # for pt in cntr:
            #     ax0[1].plot(pt[0], pt[1], 'ks')

            # plt.savefig('./c=%d__lambda=%f.png'%(no_cluster, lambda_rad))
            # # plt.show()
            # plt.close()

    # plot (no_cluster, lambda_rad, accuracy)
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = [c for c in cluster_range]
    Y = [l for l in lambda_range]
    X, Y = np.meshgrid(X, Y)
    Z = np.ndarray(X.shape)
    for idx0 in range(X.shape[0]):
        for idx1 in range(X.shape[1]):
            X_val = str(X[idx0, idx1])
            Y_val = f"{Y[idx0, idx1]:.1f}"
            try:
                Z[idx0, idx1] = accuracy_dict[X_val+'+'+Y_val][2]
            except KeyError:
                print('error')
                print('no_clusters: ' + X_val)
                print('lambda: ' + Y_val)
            

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('coolwarm'), linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(0, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.savefig('./variation.png')
    # plt.show()
    plt.close()

    # Visualize the best model and rebuild
    # select max(no_cluster, lambda_rad)
    max_idx = np.unravel_index(np.argmax(Z, axis=None), Z.shape) 

    no_cluster = X[max_idx]
    lambda_rad = Y[max_idx]
    cntr, u = fcm(train_data, no_cluster)
    # u = (no_cluster, train_size)
    # cntr = (no_cluster, data_shape)
    # train_data = (data_shape, train_size)
    # labels = (alldata_size,)

    # calc G
    G = np.zeros(shape=(train_size, no_cluster))
    
    for j in range(no_cluster):
        temp0 = []
        for temp_idx in range(train_size):
            temp1 = train_data[:, temp_idx] - cntr[j]
            temp1 = (u[j][temp_idx]**u_exponent) * np.matmul(temp1.T, temp1)
            temp0.append(temp1)
        C = sum(temp0) / (sum([x**u_exponent for x in u[j]]))
        for i in range(train_size):
            temp0 = train_data[:, i] - cntr[j]
            temp1 = exp(-1 * lambda_rad * np.matmul(temp0.T, temp0) * C)
            G[i, j] = temp1
    
    # calc W
    Y = np.zeros(shape=(train_size, no_class_types))
    for temp_idx in range(train_size):
        temp0 = y_train[temp_idx]
        Y[temp_idx, temp0] = 1

    GtG_1 = np.linalg.inv(np.matmul(G.T, G))
    GtG_1G = np.matmul(GtG_1, G.T)
    W = np.matmul(GtG_1G, Y)

    # y~
    GW = np.matmul(G, W).T
    y_pred = np.argmax(GW, axis=0)

    # accuracy
    false_pred = np.sum(np.abs(np.sign(y_train - y_pred)))
    accuracy = 1 - false_pred/train_size
    print('no_clusters=%d; lambda=%f; accuracy on train data=%f'%(no_cluster, lambda_rad, accuracy))

    # predict on test data:
    test_data = X_test.T
    test_size = len(X_test)
    G_testdata = np.zeros(shape=(test_size, no_cluster))
    
    u_testdata = calc_u(test_data, cntr)

    for j in range(no_cluster):
        temp0 = []
        for temp_idx in range(test_size):
            temp1 = test_data[:, temp_idx] - cntr[j]
            temp1 = (u_testdata[j][temp_idx]**u_exponent) * np.matmul(temp1.T, temp1)
            temp0.append(temp1)
        C = sum(temp0) / (sum([x**u_exponent for x in u_testdata[j]]))
        for i in range(test_size):
            temp0 = test_data[:, i] - cntr[j]
            temp1 = exp(-1 * lambda_rad * np.matmul(temp0.T, temp0) * C)
            G_testdata[i, j] = temp1

    # y~
    Gbar_x_W = np.matmul(G_testdata, W).T
    y_pred_test_data = np.argmax(Gbar_x_W, axis=0)

    # accuracy
    false_pred = np.sum(np.abs(np.sign(y_test - y_pred_test_data)))
    accuracy = 1 - false_pred/test_size
    print('no_clusters=%d; lambda=%f; accuracy on test data=%f'%(no_cluster, lambda_rad, accuracy))

    # # Visualize the test data
    colors = ['g', 'b', 'orange', 'c', 'm', 'y', 'Tan', 'Brown', 'DarkRed', 'ForestGreen', 'r', 'Peru', 'Gold', 'HotPink', 
                'Pink', 'Silver', 'Indigo', 'Navy', 'Turquoise', 'Olive', 'SeaGreen']
    no_all_colors = len(colors)
    fig0, ax0 = plt.subplots(2, 1)
    for label in range(no_class_types):
        ax0[0].plot(xpts[labels == label], ypts[labels == label], '.', color=colors[label])
    for label in range(no_class_types):
        select_true_preds = []
        select_false_preds = []
        for pred, true_label in zip(y_pred_test_data, y_test):
            select_true_preds.append(pred == true_label and true_label == label)
            select_false_preds.append(pred != true_label and true_label == label)
        ax0[1].plot(test_data[0][select_true_preds], test_data[1][select_true_preds], '.', color=colors[label])
        ax0[1].plot(test_data[0][select_false_preds], test_data[1][select_false_preds], '.', color='r')

    ax0[0].set_title('original labels(no_clusters=%d; lambda=%f)'%(no_cluster, lambda_rad))
    ax0[1].set_title('model on test data(no_clusters=%d; lambda=%f)'%(no_cluster, lambda_rad))
    # Mark the center of each fuzzy cluster
    for pt in cntr:
        ax0[1].plot(pt[0], pt[1], 'ks')

    plt.savefig('./c=%d__lambda=%f.png'%(no_cluster, lambda_rad))
    plt.close()

    # plotting cluster boundries
    # Generate uniformly sampled data spread across the range [0, 10] in x and y
    newdata = np.random.uniform(-5, 20, (2500, 2))

    # Predict new cluster membership with `cmeans_predict` as well as
    # `cntr` from the 3-cluster model
    u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(newdata.T, cntr, u_exponent, error=0.005, maxiter=1000)

    # Plot the classified uniform data. Note for visualization the maximum
    # membership value has been taken at each point (i.e. these are hardened,
    # not fuzzy results visualized) but the full fuzzy result is the output
    # from cmeans_predict.
    cluster_membership = np.argmax(u, axis=0)  # Hardening for visualization

    fig3, ax3 = plt.subplots()
    ax3.set_title('cluster boundries')
    for j in range(len(cntr)):
        ax3.plot(newdata[cluster_membership == j, 0],
                newdata[cluster_membership == j, 1], 'o',
                color=colors[j%no_all_colors])

    # Mark the center of each fuzzy cluster
    for pt in cntr:
        ax3.plot(pt[0], pt[1], 'ks')

    plt.savefig('./best_clustering_boundries.png')
    plt.close()