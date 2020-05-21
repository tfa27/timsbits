import random
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


class Centroids:
    def __init__(self, k_init, data_init):
        self.centroids = np.zeros((k_init, 2))
        self.k = k_init
        indexes = []
        for i_cent in range(0, k):
            done = False
            while done is False:
                idx = random.randint(0, data_init.shape[0])
                if idx not in indexes:
                    indexes.append(idx)
                    self.centroids[i_cent, 0] = data_init[i_cent, 0]
                    self.centroids[i_cent, 1] = data_init[i_cent, 1]
                    done = True

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

    def train_algorithm(self, data_train, iterations):
        different_k_s = []
        for it in range(iterations):
            for little_k in range(self.k):
                self.calculate_mean_cluster_assign(data_train)
                data_k = data_train[data_train[:, 2] == little_k + 1]
                if iterations - it == 1:
                    different_k_s.append(data_k)
                self.centroids[little_k, 0] = calc_mean(list(data_k[:, 0]))
                self.centroids[little_k, 1] = calc_mean(list(data_k[:, 1]))
        return different_k_s


def calc_mean(list_for_mean):
    length = len(list_for_mean)
    sum_mean = 0
    for row in range(length):
        sum_mean += list_for_mean[row]
    mean_ = sum_mean / length
    return mean_


df = pd.read_csv(r'C:\Users\User\Desktop\datasets\Mall_Customers.csv')
cols_to_keep = ['Annual Income (k$)', 'Spending Score (1-100)']
df = df[cols_to_keep]
dat = df.to_numpy()
m = dat.shape[0]
n = dat.shape[1]
data = np.zeros((m, n+1))
data[:, 0:n] = dat
k = 5
these_cents = Centroids(k, data)

datas = these_cents.train_algorithm(data, iterations=10)
colours = ['r', 'g', 'b', 'y', 'm']

for plott in range(k):
    plt.scatter(datas[plott][:, 0], datas[plott][:, 1], color=colours[plott], alpha=0.1)
    plt.scatter(these_cents.centroids[plott, 0], these_cents.centroids[plott, 1], color=colours[plott])
plt.title("Simple K-Means Algorithm")
plt.show()
