#  this was a coding challenge for a job I went for.


def string_perm_check(str1, str2):  # create function for the sake of tidiness and ability to call upon
    permed = True  # set variable to True initially
    for i in str1:  # iterate through str1, could be str2 doesn't matter which way round it is done
        if str1.count(i) != str2.count(i):  # count each character in each string and check the count is the same.
            permed = False  # set output variable to false if the character count is different
    if len(str2) != len(str1):  # compare lengths
        permed = False  # if lengths are different they cannot be permutations
    return permed  # return output variable


# computation complexity at a minimum, only two iterative steps to determine if the
# strings are permutations of one another
inp1 = 'this is a test to check if these strings are permutations'
inp2 = 'permutations are strings these if check to test a is this'
# deliberately added a few more characters and changed order ^
if string_perm_check(inp1, inp2) is True:
    print('These strings are permutations of one another!')
else:
    print('These strings are not permutations of one another!')
