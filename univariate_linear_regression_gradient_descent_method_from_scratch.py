#  uni-variate linear regression algorithm. converts csv files into lists and works from there
import pandas as pd
import random
import matplotlib.pyplot as plt


def get_data_and_split(train_frac):
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
            x_train = x_all_random[0:(round((len(x_all_random) * train_frac)))]
            x_test = x_all_random[(round((len(x_all_random) * train_frac))):-1]
            y_train = y_all_random[0:(round((len(x_all_random) * train_frac)))]
            y_test = y_all_random[(round((len(x_all_random) * train_frac))):-1]
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


def scaling_function(f):
    if len(f) != len(f):
        print("nah. ")
    else:
        max_f = max(f)
        min_f = min(f)
        for i in range(0, len(f)):
            f[i] /= (max_f - min_f)
        return f


def cost_function(predicted, labels_cost):
    cost_sum = 0
    for i in range(len(predicted)):
        cost_sum += (predicted[i] - labels_cost[i]) ** 2
    cost = (1 / (2 * len(predicted))) * cost_sum
    return cost


def gradient_descent(features_grad, labels_grad, alpha):
    costs = []
    theta_zero = 1
    theta_one = 1
    m = len(features_grad)
    decider = False
    while decider is False:
        h = []
        for i in range(0, len(features_grad)):
            h.append(theta_zero + (theta_one * features_grad[i]))
        costs.append(cost_function(h, labels_grad))
        if len(costs) > 1:
            if costs[-2] - costs[-1] < 0.001:
                return h, costs
        bracket_theta_zero = 0
        bracket_theta_one = 0
        for n in range(0, len(features_grad)):
            bracket_theta_zero += (h[n] - labels_grad[n])
            bracket_theta_one += (h[n] - labels_grad[n]) * features_grad[n]
        temp_theta_zero = theta_zero - alpha * ((1 / m) * bracket_theta_zero)
        temp_theta_one = theta_one - alpha * ((1 / m) * bracket_theta_one)
        theta_zero = temp_theta_zero
        theta_one = temp_theta_one
        print("New theta 0: " + str(theta_zero) + " | " + "New theta 1: " + str(theta_one) + ' | ' +
              "Cost value: " + str(costs[-1]) + '\n')


def lin_reg_main():
    learning_rate = float(input("Enter your learning rate: "))
    training_fraction = float(input("Enter training fraction as decimal: "))
    features_train, features_test, labels_train, labels_test = get_data_and_split(training_fraction)
    features_train_scaled = scaling_function(features_train)
    hypothesis, list_of_costs = gradient_descent(features_train_scaled, labels_train, learning_rate)
    print("Final cost: " + str(list_of_costs[len(list_of_costs) - 1]))
    plt.scatter(features_train_scaled, labels_train)
    plt.plot(features_train, hypothesis, color='red')
    plt.show()
    plt.close()


lin_reg_main()


#  /Users/timandersson1/Desktop/jupyter files/kc_house_data.csv
#  ^^^ this is the data set I was using to test the algorithm.
#  /Users/timandersson1/Desktop/jupyter files/Iris.csv

#  https://drive.google.com/open?id=1AudFeE7dbUS2nPvUFIuasKgpEtuSdroM
#  https://drive.google.com/open?id=1_h8NFCJv-jNc4BmjGkPG-tPHEA_HuZLU
#  ^^^ for testing.
