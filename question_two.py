#  Another question I did for a job a while back. 
#  Had to take a list of numbers between 1 and 1 million, and count all the missing ones. 


def question_two(list1):
    ints = list(range(1, 1000000))  # list in the appropriate range
    for i in list1:  # iterate through input list
        if i in ints:  # if statement to handle any duplicates in input list
            ints.remove(i)  # simply remove the element from the list
    return ints  # return the ints variable containing all missing numbers in the appropriate range


def validate(input_list, output_list):  # function to validate the above function
    check = []  # create a list
    val = bool  # initiate output variable
    for i in input_list:  # iterate through the shorter list
        if i in output_list:  # iterate through longer list to check no same values exist in both
            check.append(i)  # if same value in both lists, append value to check list
    if len(check) == 0:  # if the check list is empty, the function has worked
        val = True  # set val to true meaning the function has worked
    elif len(check) > 0:  # if check list is not empty function has not worked
        val = False
    return val


def create_list():
    # creating a random list of integers in appropriate range
    from random import randint
    lst = []
    n = 2
    while n < 1001:  # list of 1 thousand integers so there's a higher probability of duplicates than 100
        lst.append(randint(1, 1000000))
        n += 1
    return lst


inp_list = create_list()
# using a second function to double check the lists don't have any of the same values
if validate(inp_list, question_two(inp_list)) is True:
    print('Program works.')
else:
    print('Program failed.')
