#  uni-variate linear regression algorithm. converts csv files into lists and works from there
import pandas as pd
import random
import matplotlib.pyplot as plt


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


def gradient_descent(features, labels, alpha):
    theta_zero = random.random()
    theta_one = random.random()
    h = list
    difference = 1
    dif_previous = 1
    bracket_sum_zero = 0
    bracket_sum_one = 0
    while difference > 0.0001:
        h = []
        for i in range(0, len(features)):
            h.append(theta_zero + (theta_one * features[i]))
        for k in range(0, len(features)):
            bracket_sum_zero += h[k] - labels[k]
            bracket_sum_one += (h[k] - labels[k]) * k
        difference = (dif_previous - (bracket_sum_zero + bracket_sum_one))
        dif_previous = bracket_sum_one + bracket_sum_zero
        print(difference)
        temp_zero = theta_zero - ((alpha / (len(features))) * bracket_sum_zero)
        temp_one = theta_one - ((alpha / (len(features))) * bracket_sum_one)
        theta_zero = temp_zero
        theta_one = temp_one
        print("Theta 0: " + str(theta_zero) + " Theta 1: " + str(theta_one))
    return h


learning_rate = 0.001
features_train, features_test, labels_train, labels_test = get_data_set(0.7)
features_train_scaled = feature_scaling(features_train)
hypothesis = gradient_descent(features_train_scaled, labels_train, learning_rate)
plt.scatter(features_train_scaled, labels_train)
plt.plot(features_train, hypothesis, color='red')
plt.show()
plt.close()

#  /Users/timandersson1/Desktop/jupyter files/kc_house_data.csv
#  ^^^ this is the data set I was using to test the algorithm.
#  /Users/timandersson1/Desktop/jupyter files/winequality-red-mod.csv
#  /Users/timandersson1/Desktop/jupyter files/Iris.csv
