#  uni-variate linear regression algorithm. converts csv files into lists and works from there
import pandas as pd
import random
import matplotlib.pyplot as plt
import time


def get_data_set(train_frac):
    print("This algorithm is for uni-variate linear regression with continuous variables only. ")
    file_path = str(input("Enter file path to data set including data set name (csv file type only): "))
    if ".csv" not in file_path:
        print("Your data-set needs to be a csv file type. ")
    else:
        data_set = pd.read_csv(file_path)
        print(data_set.info())
        label_col_name = str(input("Enter the column you wish to be the label: "))
        y_all = list(data_set[label_col_name])
        data_set = data_set.drop(axis=0, columns=label_col_name)
        if data_set.shape[1] > 2:
            x_all = list(data_set[str(input("Enter the column you wish to be the feature: "))])
        else:
            x_all = list(data_set[0])
        if len(x_all) != len(y_all):
            print("Summin ain't right here. ")
        else:
            x_all_random, y_all_random = randomize_list_order(x_all, y_all)
            train_num = round((len(x_all_random) * train_frac))
            x_train = x_all_random[0:train_num]
            x_test = x_all_random[train_num:-1]
            y_train = y_all_random[0:train_num]
            y_test = y_all_random[train_num:-1]
            return x_train, x_test, y_train, y_test


def randomize_list_order(lst_one, lst_two):
    new_list_one = []
    new_list_two = []
    n = 0
    while n < len(lst_one):
        idx = random.randint(0, (len(lst_one) - 1))
        new_list_one.append(lst_one[idx])
        new_list_two.append(lst_two[idx])
        del lst_one[idx]
        del lst_two[idx]
    return new_list_one, new_list_two


def feature_scaling(f):
    if len(f) != len(f):
        print("nah. ")
    else:
        max_f = max(f)
        for i in range(0, len(f)):
            f[i] /= max_f
        return f


def mean(list_of_vals):
    numb = 0
    for i in range(0, len(list_of_vals)):
        numb += list_of_vals[i]
    mean_op = numb / len(list_of_vals)
    return mean_op


def linear_regression(feats, labs):
    h = []
    feats_mean = mean(feats)
    labs_mean = mean(labs)
    numerator = 0
    denominator = 0
    for i in range(0, len(feats)):
        numerator += (feats[i] - feats_mean) * (labs[i] - labs_mean)
        denominator += (feats[i] - feats_mean) ** 2
    theta_one = numerator / denominator
    theta_zero = labs_mean - (theta_one * feats_mean)
    for k in range(0, len(feats)):
        h.append(theta_zero + (theta_one * feats[k]))
    return h


# learning_rate = 0.00001
features_train, features_test, labels_train, labels_test = get_data_set(0.7)
features_train_scaled = feature_scaling(features_train)
# labels_train_scaled = feature_scaling(labels_train)
hypothesis = linear_regression(features_train_scaled, labels_train)
plt.scatter(features_train_scaled, labels_train)
plt.plot(features_train, hypothesis, color='red')
plt.show()
plt.close('all')

#  /Users/timandersson1/Desktop/jupyter files/kc_house_data.csv
#  ^^^ this is the data set I was using to test the algorithm.
#  /Users/timandersson1/Desktop/jupyter files/winequality-red-mod.csv
#  /Users/timandersson1/Desktop/jupyter files/Iris.csv
