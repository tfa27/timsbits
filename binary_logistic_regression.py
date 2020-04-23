import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd


def euler():
    n = 1000000
    euler_num = (1 + (1/n))**n
    return euler_num


def sigmoid(z_sig):
    sig = np.zeros((z_sig.shape[0], 1))
    for iterate in range(z_sig.shape[0]):
        sig[iterate, 0] = (1 / (1 + (euler()**-z_sig[iterate])))
    return sig


def cost_function(label, hypothesis):
    m = label.shape[0]
    summation = 0
    for _cost in range(0, label.shape[0]):
        h_i = hypothesis[_cost, 0]
        y_i = label[_cost, 0]
        if y_i == 0:
            summation += (- ((1 -y_i) * np.log(1 - h_i)))
        elif y_i == 1:
            summation += (-y_i * np.log(h_i))
    j = summation / m
    return j


def gradient_descent(theta_, X_, y_, alpha, iter):
    temp_theta = np.zeros((theta_.shape[0], 1))
    m_ = X_.shape[0]
    p = 0
    while p < iter:
        z_ = np.matmul(X_, theta_)
        h_ = sigmoid(z_)
        for i in range(0, theta_.shape[0]):
            summation = 0
            for a in range(0, X_.shape[0]):
                summation += (h_[a, 0] - y_[a, 0]) * X_[a, i]
            temp_theta[i, 0] = theta_[i, 0] - ((alpha / m_) * summation)
        cost_ = cost_function(y_, h_)
        print(f"Cost: {cost_} | Iteration: {p + 1}")
        theta_ = temp_theta
        p += 1
    return theta_, h_


def normalise_features(features_matrix):
    feat_shape = features_matrix.shape
    features_normalised = np.zeros((feat_shape))
    for a in range(feat_shape[1]):
        lst = list(features_matrix[:, a])
        max_val = max(lst)
        for d in range(feat_shape[0]):
            lst[d] = ((lst[d] / max_val) * 2) - 1
            features_normalised[d, a] = float(lst[d])
    return features_normalised


def logistic_regression(file_path, learning_rate, iterations):
    data = pd.read_csv(file_path)
    y = np.zeros((284807, 1))
    label = list(data["Class"])
    for x in range(len(label)):
        y[x, 0] = label[x]
    features = data.drop(["Class"], axis=1)
    X_raw = features.to_numpy()
    theta = np.zeros((X_raw.shape[1], 1))
    X = normalise_features(X_raw)
    frac_num = round((X.shape[0]) * 0.7)
    X_train = X[0:frac_num, :]
    X_test = X[frac_num:X.shape[0], :]
    y_train = y[0:frac_num, :]
    y_test = y[frac_num:y.shape[0], :]
    print(f"X_train length: {X_train.shape[0]} | "
          f"y_train length: {y_train.shape[0]} | X_test length: {X_test.shape[0]} "
          f"| y_test length: {y_test.shape[0]}")
    theta, h = gradient_descent(theta, X_train, y_train, learning_rate, iterations)
    shape_h = h.shape
    y_pred = np.zeros((y_test.shape[0], 1))
    z_test = np.matmul(X_test, theta)
    h_test = sigmoid(z_test)
    for q in range(h_test.shape[0]):
        if h_test[q, 0] >= 0.5:
            y_pred[q, 0] = 1
        elif h_test[q, 0] < 0.5:
            y_pred[q, 0] = 0
    accuracy = 0
    for v in range(h_test.shape[0]):
        if y_pred[v, 0] == y_test[v, 0]:
            accuracy += 1
        elif y_pred[v, 0] != y_test[v, 0]:
            accuracy = accuracy
    print(f"Accuracy: {accuracy / y_pred.shape[0]} / {1}")
    return theta


file = '/Users/timandersson1/Desktop/jupyter files/creditcard.csv'
t = logistic_regression(file, 0.1, 20)
