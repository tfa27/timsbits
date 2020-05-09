import pandas as pd
import numpy as np
import progressbar
import warnings
import math


def sigmoid(z_sig):
    return 1.0 / (1 + np.exp(-z_sig))


def initialise_weights(h_l, outputs, no_of_features):
    thetas = []
    for lay in range(h_l):
        thetas.append(np.random.uniform(low=-epsilon, high=epsilon, size=(no_of_features, no_of_features)))
    thetas.append(np.random.uniform(low=-epsilon, high=epsilon, size=(no_of_features, outputs)))
    return thetas


# need to add everything in one loop realistically
def forward_propagation(x_idx, x_, hidden, thetas):
    a = []
    a.append(x_[x_idx, :].reshape((x_[x_idx, :].shape[0], 1)))
    for output in range(hidden):
        a[output][0, 0] = 1
        a.append(sigmoid(np.matmul(thetas[output], a[output])))
    a.append(sigmoid(np.matmul(thetas[-1].T, a[-1])))
    return thetas, a


def nn_cost_function(K, y_cost, op_layer):
    summation = 0
    zzz = 0
    y_vec = np.zeros((K, 1))
    y_vec[y_cost, 0] = 1
    for k in range(K):
        y_i_k = y_vec[k, 0]
        h_i_k = op_layer[k, 0]
        if y_i_k == 1:
            zzz = -np.log(h_i_k)
        elif y_i_k == 0:
            zzz = -np.log(1 - h_i_k)
        summation += zzz
    return summation


def cost_regularization(theta_list, lambda_, m):
    theta_sum = 0
    for theta_idx in range(len(theta_list)):
        theta_mat = theta_list[theta_idx]
        for theta_row in range(theta_mat.shape[0]):
            for theta_col in range(theta_mat.shape[1]):
                this_theta = theta_mat[theta_row, theta_col]
                theta_sum += this_theta ** 2
    reg = (lambda_ / (2 * m)) * theta_sum
    return reg


def sigmoid_gradient(matrix):
    g = np.zeros(matrix.shape)
    for ro in range(matrix.shape[0]-1):
        for col in range(matrix.shape[1]-1):
            g_z = 1 / (1 + math.exp(-matrix[ro, col]))
            g[row, col] = g_z * (1 - g_z)
    return g


def back_propagation(theta_back_prop, activation_layers, y_back_prop, i):
    no_of_layers = len(activation_layers)
    k = activation_layers[-1].shape[0]
    y_vec = np.zeros((k, 1))
    y_vec[y_back_prop, 0] = 1
    little_delta = []
    little_delta.append(activation_layers[-1] - y_vec)
    for layer in range(1, no_of_layers):
        little_delta.append((np.matmul(theta_back_prop[-layer], little_delta[layer-1]))
                            * sigmoid_gradient(np.matmul(theta_back_prop[-layer], activation_layers[-layer]))) # need to do sigmoid gradient
    # for delt in range(len(little_delta)):
    #     little_delta[delt] = little_delta[delt][1:, :]
    big_delta = []
    for d in range(len(theta_back_prop)):
        big_delta.append(np.zeros(theta_back_prop[d].shape))
        big_delta[d] += np.matmul(little_delta[d + 1], activation_layers[d + 1].T)
    return little_delta[::-1], big_delta


warnings.filterwarnings("ignore", category=RuntimeWarning)

# file_path = r"C:\Users\User\Desktop\datasets\creditcard.csv"
file_path = r"C:\Users\User\Desktop\datasets\winequality-red-mod.csv"
data = pd.read_csv(file_path)
data = data.drop(["country"], axis=1)
data = data.drop(["id"], axis=1)
data = data.sample(frac=1)

# print(data.info())
# print(data.describe())
output_classes = 6
hidden_layers = 1
# y_df = data["Class"]
# X_df = data.drop(["Class"], axis=1)
y_df = data["quality"]
X_df = data.drop(["quality"], axis=1)
X = X_df.to_numpy()
X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
y = y_df.to_numpy()
y = np.where(y == 3, 0, y)
y = np.where(y == 4, 1, y)
y = np.where(y == 5, 2, y)
y = np.where(y == 6, 3, y)
y = np.where(y == 7, 4, y)
y = np.where(y == 8, 5, y)
y = y.reshape((X.shape[0], 1))

# print(min(list(y)))
# print(max(list(y)))
epsilon = 0.1
pred = np.zeros((X.shape[0], 1))

all_thetas = initialise_weights(h_l=hidden_layers, outputs=output_classes, no_of_features=X.shape[1])

step = X.shape[0] / 100
step_idx = 1

bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
j_val = 0
j = 0
nan_rows = []
for row in range(X.shape[0]):
    theta_all, layers = forward_propagation(row, X, hidden_layers, all_thetas)
    j = nn_cost_function(output_classes, y[row, 0], layers[-1])
    if math.isnan(j) is True:
        j_val = j_val
        nan_rows.append(row)
    elif math.isnan(j) is False:
        j_val += j
    delta = back_propagation(theta_all, layers, y, row)
    if output_classes == 1:
        op = layers[-1]
        if op >= 0.5:
            pred[row, 0] = 1
        elif op < 0.5:
            pred[row, 0] = 0
    if output_classes >= 3:
        op_list = list(layers[-1])
        m_val = max(op_list)
        idx = op_list.index(m_val)
        pred[row, 0] = idx
    if row >= step * step_idx:
        bar.update(step_idx)
        step_idx += 1
bar.finish()
j_val = j_val / (X.shape[0])
j_val += cost_regularization(theta_all, 0.001, X.shape[0])
print(f"Forward propagation done. Output layer shape: {layers[-1].shape} | Cost: {j_val}")
for thet in range(len(layers)):
    print(f"Size of activation layer {thet}: {layers[thet].shape}")
    print(f"Size of little delta layer {thet}: {delta[0][thet].shape}")
    if thet < len(theta_all):
        print(f"Size of theta {thet}: {theta_all[thet].shape}")
        print(f"Size of big delta layer {thet}: {delta[1][thet].shape}")
