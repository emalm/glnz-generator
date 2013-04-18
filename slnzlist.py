#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

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

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def determinant(matrix):
    if matrix == []:
        return 1
    elif len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        trows = [row[1:] for row in matrix]
        sum = 0
        sign = 1
        for index in xrange(len(matrix)):
            sum += sign * matrix[index][0] * determinant(trows[:index] + trows[index + 1:])
            sign *= -1
        return sum

def det_three_by_three(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
            - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
            - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
            - matrix[1][1] * matrix[2][0])
        )

def matrix_has_positive_rows(matrix):
    for row in matrix:
        if not row_is_positive(row):
            return False
    return True

def row_is_positive(row):
    for element in row:
        if element < 0:
            return False
        elif element > 0:
            break
        elif element == 0:
            continue
    return True

def rows_in_lex_order(first_row, second_row):
    for a, b in zip(first_row, second_row):
        if a < b:
            return False
        elif a > b:
            break
        elif a == b:
            continue
    return True

def matrix_rows_are_in_lex_order(matrix):
    for i in range(len(matrix) - 1):
        if not rows_in_lex_order(matrix[i], matrix[i + 1]):
            return False
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

def generate_lattice_matrices_in_shell(columns, rows, distsquared):
    if rows == 0:
        if distsquared == 0:
            yield []
    elif rows > 0:
        for i in range(distsquared):
            row_generator = generate_lattice_shell(columns, distsquared - i)
            for row in row_generator:
                if not row_is_positive(row):
                    continue
                submatrix_shell = generate_lattice_matrices_in_shell(columns, rows - 1, i)
                for submatrix in submatrix_shell:
                    if len(submatrix) == 0:
                        yield [row]
                    elif rows_in_lex_order(row, submatrix[0]):
                        yield [row] + submatrix


def generate_lattice_matrices_in_shell_alt(columns, rows, distsquared):
    for elementlist in generate_lattice_shell(columns * rows, distsquared):
        mat = [elementlist[columns * i:columns * (i + 1)] for i in range(rows)]
        if matrix_has_positive_rows(mat) and matrix_rows_are_in_lex_order(mat):
            yield mat

def main(argv = None):
    """Main routine for the script."""
    if argv is None:
        argv = sys.argv

    count = 0
    totalcount = 0

    time_start = time.clock()
    for distsquared in range(0, 10):
        for l in generate_lattice_shell(16, distsquared):
            mat = [l[0:4], l[4:8], l[8:12], l[12:16]]
            totalcount += 1

            if not matrix_has_positive_rows(mat) or not matrix_rows_are_in_lex_order(mat):
                continue

            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                # print det
                # print_matrix(transpose(mat))
                # print
    time_end = time.clock()
    print time_end - time_start

    print count, totalcount

    count = 0
    totalcount = 0

    time_start = time.clock()
    for distsquared in range(0, 10):
        for mat in generate_lattice_matrices_in_shell(4, 4, distsquared):
            totalcount += 1
            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                # print det
                # print_matrix(transpose(mat))
                # print
    time_end = time.clock()
    print time_end - time_start

    print count, totalcount

    count = 0
    totalcount = 0

    time_start = time.clock()
    for distsquared in range(0, 10):
        for mat in generate_lattice_matrices_in_shell_alt(4, 4, distsquared):
            totalcount += 1
            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                # print det
                # print_matrix(transpose(mat))
                # print
    time_end = time.clock()
    print time_end - time_start

    print count, totalcount


if __name__ == '__main__':
    sys.exit(main())
