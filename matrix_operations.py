from random import randint


def create_random_matrix(rows_create, columns_create):
    if rows_create < 1 or columns_create < 1:
        print("Invalid. Try again. ")
        exit()
    matrix_create = [[randint(0, 10) for x in range(columns_create)] for y in range(rows_create)]
    return matrix_create


def create_specific_matrix():
    rows_specific = int(input("Enter number of rows: "))
    columns_specific = int(input("Enter number of columns: "))
    matrix_specific = [[0 for x in range(columns_specific)] for y in range(rows_specific)]
    for n_create_matrix in range(0, rows_specific):
        for m_create_matrix in range(0, columns_specific):
            matrix_specific[n_create_matrix][m_create_matrix] = \
                int(input("Value for position (" + str(n_create_matrix) + ", " + str(m_create_matrix) + "): "))
    return matrix_specific


def print_matrix(matrix_print):
    for i_print in range(0, len(matrix_print)):
        print(matrix_print[i_print])


def det_a(matrix_det_a):
    if len(matrix_det_a) != len(matrix_det_a[0]):
        print('Determinants are only defined for square matrices. ')
    else:
        lst_det_a = []
        matrix_det_a_rref = rref(matrix_det_a)
        for n_det_a in range(0, (len(matrix_det_a_rref))):
            lst_det_a.append(matrix_det_a_rref[n_det_a][n_det_a])
        result_det_a = 1
        for x in lst_det_a:
            result_det_a *= x
        return result_det_a


def rref(matrix_rref):
    if matrix_rref[0][0] == 0:
        matrix_rref[0] = matrix_rref[len(matrix_rref) - 1]
        matrix_rref[len(matrix_rref) - 1] = matrix_rref[0]
    for n_rref in range(0, (len(matrix_rref))):
        for i in range(n_rref+1, len(matrix_rref)):
            new_line_rref = []
            for x in range(0, len(matrix_rref[0])):
                new_line_rref.append(matrix_rref[i][x]-((matrix_rref[n_rref][x]) *
                                                        (matrix_rref[i][n_rref] / matrix_rref[n_rref][n_rref])))
            matrix_rref[i] = new_line_rref
    matrix_rref = remainder_destroyer(matrix_rref)
    return matrix_rref


def identity_matrix(rows_i, columns_i):
    if rows_i != columns_i:
        print('Identity matrices must be square. ')
    else:
        identity_matrix_from_func = [[0 for x in range(columns_i)] for y in range(rows_i)]
        for n_identity in range(0, rows_i):
            identity_matrix_from_func[n_identity][n_identity] = 1
        return identity_matrix_from_func


def matrix_multiplier(matrix_1, matrix_2):
    if len(matrix_1[0]) != len(matrix_2):
        print('These matrices cannot be multiplied/cannot be multiplied in this order. ')
    else:
        m_out_multiplier_func = [[0 for x in range(len(matrix_2[0]))] for y in range(len(matrix_1))]
        for n_multiplier_func in range(0, len(matrix_1)):
            for m_multiplier_func in range(0, len(matrix_2[0])):
                lst_rows = matrix_1[n_multiplier_func]
                lst_cols = []
                for p_multiplier_func in range(0, len(matrix_2)):
                    lst_cols.append(matrix_2[p_multiplier_func][m_multiplier_func])
                new_inp_multiplier_func = []
                d1 = 0
                d2 = 0
                while d1 < len(lst_rows) and d2 < len(lst_cols):
                    new_inp_multiplier_func.append(lst_rows[d1] * lst_cols[d2])
                    d1 += 1
                    d2 += 1
                result_multiplier_func = 0
                for i in new_inp_multiplier_func:
                    result_multiplier_func += i
                m_out_multiplier_func[n_multiplier_func][m_multiplier_func] = result_multiplier_func
        m_out_multiplier_func = remainder_destroyer(m_out_multiplier_func)
        return m_out_multiplier_func


def remainder_destroyer(matrix_remainders):
    for i in range(0, len(matrix_remainders)):
        for n in range(0, len(matrix_remainders[0])):
            if -0.00000001 < matrix_remainders[i][n] < 0.00000001:
                matrix_remainders[i][n] = 0
            elif 0.999 < matrix_remainders[i][n] < 1.0001:
                matrix_remainders[i][n] = 1
    return matrix_remainders


def row_swap(matrix_row_swap, i_row_swap):
    zero_line_invert_function = matrix_row_swap[0]
    matrix_row_swap[0] = matrix_row_swap[len(matrix_row_swap) - 1]
    matrix_row_swap[len(matrix_row_swap) - 1] = zero_line_invert_function
    zero_i_invert_function = i_row_swap[0]
    i_row_swap[0] = i_row_swap[len(matrix_row_swap) - 1]
    i_row_swap[len(matrix_row_swap) - 1] = zero_i_invert_function
    return matrix_row_swap, i_row_swap


def invert_matrix(your_matrix):
    i_invert_function = identity_matrix(len(your_matrix), len(your_matrix[0]))
    your_matrix, i_invert_function = row_swap(your_matrix, i_invert_function)
    is_linear = check_linearly_dependent(your_matrix)
    if is_linear is False:
        for n_invert_func in range(0, (len(your_matrix))):
            for i in range(n_invert_func + 1, len(your_matrix)):
                new_line_invert_function = []
                new_zero_invert_function = []
                for x_invert_function in range(0, len(your_matrix[0])):
                    if your_matrix[n_invert_func][n_invert_func] == 0:
                        your_matrix, i_invert_function = row_swap(your_matrix, i_invert_function)
                    new_line_invert_function.append(your_matrix[i][x_invert_function] -
                                                    ((your_matrix[n_invert_func][x_invert_function]) *
                                                     (your_matrix[i][n_invert_func]
                                                      / your_matrix[n_invert_func][n_invert_func])))
                    new_zero_invert_function.append(i_invert_function[i][x_invert_function] -
                                                    ((i_invert_function[n_invert_func][x_invert_function]) *
                                                     (your_matrix[i][n_invert_func] /
                                                      your_matrix[n_invert_func][n_invert_func])))
                your_matrix[i] = new_line_invert_function
                i_invert_function[i] = new_zero_invert_function
        n_invert_func = len(your_matrix) - 1
        t_invert_function = 0 + ((len(your_matrix) - 1) - n_invert_func)
        while t_invert_function < (len(your_matrix) - 1):
            z_invert_function = 1
            while z_invert_function < len(your_matrix) - t_invert_function:
                scalar_invert_function = your_matrix[n_invert_func - z_invert_function][n_invert_func] / \
                                         your_matrix[n_invert_func][n_invert_func]
                for y_invert_function in range(0, (len(your_matrix[n_invert_func - z_invert_function]))):
                    your_matrix[n_invert_func - z_invert_function][y_invert_function] = \
                        your_matrix[n_invert_func - z_invert_function][y_invert_function] \
                        - (your_matrix[n_invert_func][y_invert_function]
                           * scalar_invert_function)
                    i_invert_function[n_invert_func - z_invert_function][y_invert_function] = \
                        i_invert_function[n_invert_func - z_invert_function][y_invert_function] \
                        - (i_invert_function[n_invert_func][y_invert_function]
                           * scalar_invert_function)
                z_invert_function += 1
            t_invert_function += 1
            n_invert_func -= 1
        for n_invert_func in range(0, (len(your_matrix))):
            scalar_invert_function = 1 / your_matrix[n_invert_func][n_invert_func]
            for x_invert_function in range(0, (len(your_matrix[0]))):
                your_matrix[n_invert_func][x_invert_function] *= scalar_invert_function
                i_invert_function[n_invert_func][x_invert_function] *= scalar_invert_function
        i_invert_function = remainder_destroyer(i_invert_function)
        return i_invert_function
    else:
        print('This matrix is linearly dependant. It cannot be inverted. ')


def save_matrix(matrix_to_save):
    saved_matrix = [[0 for x in range(len(matrix_to_save[0]))] for y in range(len(matrix_to_save))]
    for i in range(0, len(matrix_to_save)):
        for n in range(0, len(matrix_to_save[0])):
            saved_matrix[i][n] = matrix_to_save[i][n]
    return saved_matrix


def check_linearly_dependent(matrix_linear_dependency):
    linearly_dependent = False
    result = 0
    for zero_rows in range(0, len(matrix_linear_dependency)):
        for zero_columns in range(0, len(matrix_linear_dependency[0])):
            result += matrix_linear_dependency[zero_rows][zero_columns]
    if result == 0:
        linearly_dependent = True
        print('Your matrix is the zero vector. ' + '\n')
        return linearly_dependent
    for check_columns in range(0, len(matrix_linear_dependency[0])):
        list_checking = []
        for check_rows in range(0, len(matrix_linear_dependency)):
            list_checking.append(matrix_linear_dependency[check_rows][check_columns])
        for i_columns in range(0, (len(matrix_linear_dependency[0]))):
            list_to_check = []
            if i_columns != check_columns:
                for i_rows in range(0, (len(matrix_linear_dependency))):
                    list_to_check.append(matrix_linear_dependency[i_rows][i_columns])
                divs = []
                for i in range(0, len(list_checking)):
                    if list_to_check[i] == 0 or list_checking[i] == 0:
                        linearly_dependent = False
                        print('Your matrix is not linearly dependant. It is therefore invertible. '
                              + '\n')
                        return linearly_dependent
                    divs.append(list_to_check[i] / list_checking[i])
                count_divs = divs.count(divs[0])
                if count_divs == len(divs):
                    print('Your matrix is linearly dependant. It is therefore not invertible. ' + '\n')
                    linearly_dependent = True
                    return linearly_dependent
    print('Your matrix is not linearly dependant. It is therefore invertible. ' + '\n')
    return linearly_dependent


a = create_random_matrix(7, 7)
a_save = save_matrix(a)

print("Matrix A: ")
print_matrix(a)
print('\n')

print("The inverted matrix: ")
a_inv = invert_matrix(a)
print_matrix(a_inv)
print('\n')

print("The saved matrix: ")
print_matrix(a_save)
print('\n')

print("Multiplying the inverted matrix by the original to get the identity matrix: ")
a_end = matrix_multiplier(a_inv, a_save)
print_matrix(a_end)
print('\n')

b = create_specific_matrix()
print("Matrix B: ")
print_matrix(b)
print('\n')
