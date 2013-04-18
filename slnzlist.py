#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime

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

def row_is_elementary(row):
    zero_count = 0
    one_count = 0
    for element in row:
        if element == 0:
            zero_count += 1
        elif element == 1:
            one_count += 1

    return (zero_count == len(row) - 1) and (one_count == 1)


def rows_in_lex_order(first_row, second_row):
    for i in range(len(first_row)):
        a = first_row[i]
        b = second_row[i]
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

# Good row caching

row_cache = {}

def generate_good_rows_in_shell(length, distsquared):
    if length not in row_cache:
        row_cache[length] = {}

    row_cache_for_length = row_cache[length]

    if distsquared not in row_cache_for_length:
        row_cache_for_length[distsquared] = []
        rows = []
        # generate rows, cache good ones
        row_generator = generate_lattice_shell(length, distsquared)
        for row in row_generator:
            if (row_is_positive(row)
                and not row_is_elementary(row)
                ):
                rows.append(row)

        # print "Generated {} rows of length {}, d2 {}".format(len(rows), length, distsquared)

        row_cache_for_length[distsquared] = rows

    for row in row_cache_for_length[distsquared]:
        yield row


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
            # distsquared - i counts down from distsquared to 1
            row_generator = generate_lattice_shell(columns, distsquared - i)
            for row in row_generator:
                if (not row_is_positive(row)
                    or row_is_elementary(row)
                    ):
                    continue

                submatrix_shell = generate_lattice_matrices_in_shell(columns, rows - 1, i)

                for submatrix in submatrix_shell:
                    if len(submatrix) == 0:
                        yield [row]
                    elif rows_in_lex_order(row, submatrix[0]):
                        yield [row] + submatrix


def generate_lattice_matrices_in_shell_with_row_cache(columns, rows, distsquared):
    if rows == 0:
        if distsquared == 0:
            yield []
    elif rows > 0:
        for i in range(distsquared):
            submatrix_shell = generate_lattice_matrices_in_shell_with_row_cache(columns, rows - 1, i)

            for submatrix in submatrix_shell:
                # distsquared - i counts down from distsquared to 1
                row_generator = generate_good_rows_in_shell(columns, distsquared - i)

                for row in row_generator:
                    if len(submatrix) == 0:
                        yield [row]
                    elif rows_in_lex_order(row, submatrix[0]):
                        yield [row] + submatrix


def test_direct_lattice_shell(length, start, stop, print_matrices=False):
    count = 0
    totalcount = 0

    row_indices = range(length)
    row_boundaries = range(0, length * length + 1, length)

    # print row_boundaries

    print "Testing matrices direct from lattice:"

    time_start = time.clock()
    for distsquared in range(start, stop):
        for entry in generate_lattice_shell(length * length, distsquared):
            totalcount += 1

            mat = [
                entry[row_boundaries[i]:row_boundaries[i + 1]]
                for i in row_indices]

            if (not matrix_has_positive_rows(mat)
                or not matrix_rows_are_in_lex_order(mat)):
                continue

            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                if print_matrices:
                    print_matrix(transpose(mat))
                    print

    time_end = time.clock()
    print "Time: {} s".format(time_end - time_start)

    print "{} valid\n{} generated\n".format(count, totalcount)

def test_direct_lattice_internal_chop(length, start, stop, print_matrices=False):
    count = 0
    totalcount = 0

    row_indices = range(length)
    row_boundaries = range(0, length * length + 1, length)

    # print row_boundaries

    print "Testing matrices with direct generation, then screening:"

    time_start = time.clock()
    for distsquared in range(start, stop):
        for mat in generate_lattice_matrices_in_shell_alt(length, length, distsquared):
            totalcount += 1

            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                if print_matrices:
                    print_matrix(transpose(mat))
                    print

    time_end = time.clock()
    print "Time: {} s".format(time_end - time_start)

    print "{} valid\n{} generated\n".format(count, totalcount)

def test_lattice_by_rows(length, start, stop, print_matrices=False):
    count = 0
    totalcount = 0

    row_indices = range(length)
    row_boundaries = range(0, length * length + 1, length)

    # print row_boundaries

    print "Testing matrices with internal row pruning (pos and elem):"

    time_start = time.clock()
    for distsquared in range(start, stop):
        for mat in generate_lattice_matrices_in_shell(length, length, distsquared):
            totalcount += 1

            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                if print_matrices:
                    print_matrix(transpose(mat))
                    print

    time_end = time.clock()
    print "Time: {} s".format(time_end - time_start)

    print "{} valid\n{} generated\n".format(count, totalcount)


def test_lattice_by_rows_with_caching(length, start, stop, print_matrices=False):
    count = 0
    totalcount = 0

    row_indices = range(length)
    row_boundaries = range(0, length * length + 1, length)

    # print row_boundaries

    print "Testing matrices with internal row pruning (pos and elem), caching:"

    time_start = time.clock()
    for distsquared in range(start, stop):
        for mat in generate_lattice_matrices_in_shell_with_row_cache(length, length, distsquared):
            totalcount += 1

            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                if print_matrices:
                    print_matrix(transpose(mat))
                    print

    time_end = time.clock()
    print "Time: {} s".format(time_end - time_start)

    print "{} valid\n{} generated\n".format(count, totalcount)


def test_suite():

    print "Testing at {}".format(datetime.datetime.now())
    print

    test_suite_matrices()

    # test_suite_row_caching()

    print "Tests finished.\n*****"
    print

def test_suite_matrices():
    arguments = {
        'length': 4,
        'start': 1,
        'stop': 12,
        'print_matrices': False
    }

    tests = [
        # test_direct_lattice_shell,
        # test_direct_lattice_internal_chop,
        test_lattice_by_rows,
        test_lattice_by_rows_with_caching,
    ]

    print "Testing matrix generation: dim {length}, start {start}, stop {stop}".format(**arguments)
    print

    for fn in tests:
        fn(**arguments)


def test_suite_row_caching():
    count = 0
    for i in range(0,17):
        for row in generate_good_rows_in_shell(4, i):
            # print row
            count += 1
    print count

    for i in range(0,17):
        for row in generate_good_rows_in_shell(4, i):
            # print row
            count += 1

    print count

def main(argv = None):
    """Main routine for the script."""
    if argv is None:
        argv = sys.argv

    test_suite()

if __name__ == '__main__':
    sys.exit(main())
