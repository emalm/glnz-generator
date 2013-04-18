#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

square_root_max = 0
square_root_list = [0]

def square_root_lookup(n):
    global square_root_max

    # current list reaches to index (square_root_max + 1)^2 - 1
    while (square_root_max + 2) * square_root_max < n:
        square_root_max += 1
        square_root_list.extend([square_root_max] * (2 * square_root_max + 1))

    return square_root_list[n]

def square_root_test():
    print square_root_lookup(0)
    print square_root_lookup(1)
    print square_root_lookup(2)
    print square_root_lookup(14)
    print len(square_root_list)

    print square_root_lookup(144)

    print square_root_lookup(146)
    print len(square_root_list)

def det_three_by_three(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
            - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
            - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
            - matrix[1][1] * matrix[2][0])
        )

def matrix_is_positive(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[j][i] < 0:
                return False
            elif matrix[j][i] > 0:
                break
            elif matrix[j][i] == 0:
                continue
    return True

def matrix_columns_are_in_lex_order(matrix):
    for i in range(len(matrix) - 1):
        for j in range(len(matrix)):
            if matrix[j][i] < matrix[j][i + 1]:
                return False
            elif matrix[j][i] > matrix[j][i + 1]:
                break
            elif matrix[j][i] == matrix[j][i + 1]:
                continue
    return True

def print_matrix(matrix):
    for row in matrix:
        print_matrix_row(row)

def print_matrix_row(row):
    print '|',
    for element in row:
        print "{:>3}".format(element),
    print '|'

def generate_lattice_shell(n, distsquared):
    if n == 0:
        if distsquared == 0:
            yield []
    elif n > 0:
        max = square_root_lookup(distsquared)
        for i in range(max, -1, -1):
            subshell = generate_lattice_shell(n - 1, distsquared - (i * i))
            for sublist in subshell:
                if i > 0:
                    yield [i] + sublist
                    yield [-i] + sublist
                else:
                    yield [0] + sublist

def main(argv = None):
    """Main routine for the script."""
    if argv is None:
        argv = sys.argv

    count = 0

    for distsquared in range(0, 25):
        for l in generate_lattice_shell(9, distsquared):
            mat = [l[0:3], l[3:6], l[6:9]]
            det = det_three_by_three(mat)
            if (det == 1 or det == -1) and matrix_is_positive(mat) and matrix_columns_are_in_lex_order(mat):
                count += 1
                # print det
                print_matrix(mat)
                print

    print count

if __name__ == '__main__':
    sys.exit(main())
