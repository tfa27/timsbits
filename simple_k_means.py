import random
import numpy as np
import matplotlib.pyplot as plt
import math


class Centroids:
    def __init__(self, k_init, x_range, y_range):
        self.centroids = np.zeros((k_init, 2))
        self.k = k_init
        for i_cent in range(0, k):
            self.centroids[i_cent, 0] = random.randint(x_range[0], x_range[1])
            self.centroids[i_cent, 1] = random.randint(y_range[0], y_range[1])

    def calculate_mean_cluster_assign(self, data_centroids):
        m_cent = data_centroids.shape[0]
        for example in range(m_cent):
            distances = []
            for k_ in range(self.k):
                distance_x = data_centroids[example, 0] - self.centroids[k_, 0]
                distance_y = data_centroids[example, 1] - self.centroids[k_, 1]
                distances.append(math.sqrt(distance_x**2 + distance_y**2))
            assigned_centroid = distances.index(min(distances)) + 1
            data[example, 2] = assigned_centroid


def random_data_gen(range_1, range_2, range_3, range_4, m_random):
    data_to_return = np.zeros((m_random, 2))
    sect = round(m_random / 2)
    for i_random in range(sect):
        data_to_return[i_random, 0] = random.randint(range_1[0], range_1[1])
        data_to_return[i_random, 1] = random.randint(range_2[0], range_2[1])
    for i_ in range(sect, m_random):
        data_to_return[i_, 0] = random.randint(range_3[0], range_3[1])
        data_to_return[i_, 1] = random.randint(range_4[0], range_4[1])
    return data_to_return


def train_algorithm(cents, data_train, iterations):
    data_k_1 = np.array([])
    data_k_2 = np.array([])
    for it in range(iterations):
        cents.calculate_mean_cluster_assign(data_train)
        data_k_1 = data_train[data_train[:, 2] == 1]
        data_k_2 = data_train[data_train[:, 2] == 2]
        new_k_1_x = calc_mean(list(data_k_1[:, 0]))
        new_k_1_y = calc_mean(list(data_k_1[:, 1]))
        new_k_2_x = calc_mean(list(data_k_2[:, 0]))
        new_k_2_y = calc_mean(list(data_k_2[:, 1]))
        cents.centroids[0, 0] = new_k_1_x
        cents.centroids[0, 1] = new_k_1_y
        cents.centroids[1, 0] = new_k_2_x
        cents.centroids[1, 1] = new_k_2_y
    return data_k_1, data_k_2


def calc_mean(list_for_mean):
    length = len(list_for_mean)
    sum_mean = 0
    for row in range(length):
        sum_mean += list_for_mean[row]
    mean_ = sum_mean / length
    return mean_


m = 100
dat = random_data_gen([5, 40], [40, 70], [45, 90], [10, 40], m)
n = dat.shape[1]
data = np.zeros((m, n+1))
data[:, 0:n] = dat
k = 2
these_cents = Centroids(k, [min(list(data[:, 0])),
                            max(list(data[:, 0]))],
                        [min(list(data[:, 1])),
                         max(list(data[:, 1]))])

data_1, data_2 = train_algorithm(these_cents, data, 10)
plt.scatter(data_1[:, 0], data_1[:, 1], color='r', alpha=0.1)
plt.scatter(data_2[:, 0], data_2[:, 1], color='b', alpha=0.1)
plt.scatter(these_cents.centroids[0, 0], these_cents.centroids[0, 1], color='r')
plt.scatter(these_cents.centroids[1, 0], these_cents.centroids[1, 1], color='b')
plt.title("Simple K-Means Algorithm")
plt.show()
