def stringpermcheck(str1, str2):  # create function for the sake of tidiness and ability to call upon
    permed = bool  # set variable to describe whether the strings are permutations of one another
    for i in str1:  # iterate through str1, could be str2 doesn't matter which way round it is done
        if str1.count(i) != str2.count(i):  # count each character in each string and check the count is the same.
            permed = False  # set output variable to false if the character count is different
    for n in str2:  # we know whether the character count is the same, but can't account for other characters in str2
        if n not in str1:  # iterate through str2 and check for characters that are in str2 but not str1
            permed = False  # any present characters that don't occur in str1 -> set permed to false
    if permed is not False:  # if the above criteria has not been met, the strings are permutations of one another
        permed = True
    return permed  # return output variable


# computation complexity at a minimum, only two iterative steps to determine if the
# strings are permutations of one another
inp1 = 'this is a test to check if these strings are permutations'
inp2 = 'permutations are strings these if check to test a is this! 3 '
# deliberately added a few more characters and changed order ^
if stringpermcheck(inp1, inp2) is True:
    print('These strings are permutations of one another!')
else:
    print('These strings are not permutations of one another!')
