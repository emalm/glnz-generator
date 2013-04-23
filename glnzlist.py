#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import argparse
import textwrap

version = '0.01'

# Square root lookups

square_root_max = 0
square_root_list = [0]

def square_root_lookup(n):
    global square_root_max

    # current list reaches to index (square_root_max + 1)^2 - 1
    while (square_root_max + 2) * square_root_max < n:
        square_root_max += 1
        square_root_list.extend([square_root_max] * (2 * square_root_max + 1))

    return square_root_list[n]


# Matrix utilities

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


def pretty_matrix(matrix):
    output = ''
    for row in matrix:
        output += pretty_matrix_row(row)
        output += '\n'

    return output

def pretty_matrix_row(row, width=3):
    output = '| '
    for element in row:
        output += "{:>3} ".format(element)
    output += '|'
    return output

# Cache good rows

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


# Lattice point enumeration

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


# Matrix generation

def generate_lattice_matrices_in_shell(columns, rows, distsquared):
    if rows == 0:
        if distsquared == 0:
            yield []
    elif rows > 0:
        for i in range(distsquared):
            submatrix_shell = generate_lattice_matrices_in_shell(columns, rows - 1, i)

            for submatrix in submatrix_shell:
                # distsquared - i counts down from distsquared to 1
                row_generator = generate_good_rows_in_shell(columns, distsquared - i)

                for row in row_generator:
                    if len(submatrix) == 0:
                        yield [row]
                    elif rows_in_lex_order(row, submatrix[0]):
                        yield [row] + submatrix

def generate_all_matrices(size, startweight, endweight):
    for wt in range(startweight, endweight + 1):
        for mat in generate_lattice_matrices_in_shell(size, size, wt):
            yield mat

# Tests

def test_lattice_by_rows(length, start, stop, print_matrices=False):
    count = 0
    totalcount = 0

    row_indices = range(length)
    row_boundaries = range(0, length * length + 1, length)

    # print row_boundaries

    print "Testing matrices with internal row pruning (pos and elem), caching:"

    time_start = time.clock()
    for distsquared in range(start, stop):
        for mat in generate_lattice_matrices_in_shell(length, length, distsquared):
            totalcount += 1

            det = determinant(mat)

            if (det == 1 or det == -1):
                count += 1
                if print_matrices:
                    print pretty_matrix(transpose(mat))
                    print

    time_end = time.clock()
    print "Time: {} s".format(time_end - time_start)

    print "{} generated\n{} with det +/-1\n".format(totalcount, count)


def test_suite():

    print "Testing at {}".format(datetime.datetime.now())
    print

    test_suite_matrices()

    # test_suite_row_caching()

    print "Tests finished.\n*****"
    print

def test_suite_matrices():
    arguments = {
        'length': 2,
        'start': 1,
        'stop': 50,
        'print_matrices': True
    }

    tests = [
        test_lattice_by_rows,
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

def test_suite_square_root():
    print square_root_lookup(0)
    print square_root_lookup(1)
    print square_root_lookup(2)
    print square_root_lookup(14)
    print len(square_root_list)

    print square_root_lookup(144)

    print square_root_lookup(146)
    print len(square_root_list)


class Formatter(object):
    @classmethod
    def start_list(cls):
        pass

    @classmethod
    def end_list(cls):
        pass

    @classmethod
    def matrix(cls, mat):
        pass

    @classmethod
    def stats(cls, stats):
        pass


class PrettyFormatter(Formatter):
    @classmethod
    def start_list(cls):
        return ""

    @classmethod
    def end_list(cls):
        return ""

    @classmethod
    def matrix(cls, mat):
        return pretty_matrix(mat) + '\n'

    @classmethod
    def stats(cls, stats):
        lines = []

        if 'dim' in stats:
            lines.append("Matrix dimension: {}".format(stats['dim']))

        if 'min_weight' in stats:
            lines.append("Starting weight: {}".format(stats['min_weight']))

        if 'max_weight' in stats:
            lines.append("Ending weight: {}".format(stats['max_weight']))

        if 'max_count' in stats:
            lines.append("Maximum to list: {}".format(stats['max_count']))

        if 'generated_matrix_count' in stats:
            lines.append("Total matrices generated: {}".format(stats['generated_matrix_count']))

        if 'valid_matrix_count' in stats:
            lines.append("Valid matrices generated: {}".format(stats['valid_matrix_count']))

        return '\n'.join(lines)

class ListFormatter(Formatter):
    @classmethod
    def start_list(cls):
        return "["

    @classmethod
    def end_list(cls):
        return "]"

    @classmethod
    def matrix(cls, mat):
        return '\t' + str(mat) + ',\n'

    @classmethod
    def stats(cls, stats):
        return str(stats)

format_lookup = {
    'pretty': PrettyFormatter,
    'p': PrettyFormatter,
    'list': ListFormatter,
    'l': ListFormatter,
}

def print_matrix_list(dim, min_weight, max_weight, format, stats, max_count=0):
    formatter = format_lookup[format]

    count_valid = 0
    count_all = 0

    check_count = (max_count > 0)

    print formatter.start_list()

    for mat in generate_all_matrices(dim, min_weight, max_weight):
        count_all += 1

        det = determinant(mat)

        if (det == 1 or det == -1):
            count_valid += 1
            print formatter.matrix(transpose(mat)),

        if check_count and count_valid >= max_count:
            break

    print formatter.end_list()

    if stats:
        stat_dict = {
            'dim': dim,
            'min_weight': min_weight,
            'max_weight': max_weight,
            'valid_matrix_count': count_valid,
            'generated_matrix_count': count_all,
        }

        if check_count:
            stat_dict['max_count'] = max_count

        print formatter.stats(stat_dict),


# Main routine

def main(argv = None):
    """Main routine for the script."""
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Enumerates integer matrices of determinant ±1, ordered by increasing
            distance-squared weight.

        Normalizations and eliminations:
        * Each column starts with a positive number.
        * Columns are listed in decreasing lexicographic order.
        * No column is a standard basis vector.
        """))

    parser.add_argument('-n', '--dim', type=int, default=3, help='matrix dimension')

    parser.add_argument('-a', '--min-weight', type=int, default=1, help='starting matrix weight')

    parser.add_argument('-z', '--max-weight', type=int, default=None, help='ending matrix weight')

    parser.add_argument('-c', '--max-count', type=int, default=0, help='maximum number of matrices to generate')

    parser.add_argument('-s', '--stats', action='store_false', help='print some stats when done')

    parser.add_argument('-f', '--format',
        choices=['pretty', 'p', 'list', 'l'],
        default='pretty',
        help='output format')
        
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s' + version)
                        
    args = parser.parse_args(argv[1:])
    # print args

    if args.max_weight is None:
        args.max_weight = args.min_weight


    print_matrix_list(**vars(args))
    
if __name__ == '__main__':
    sys.exit(main())
