#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import textwrap
from fractions import gcd

version = '0.1'

# Square root lookups

square_root_max = 0
square_root_list = [0]

def square_root_lookup(n):
    """Compute floor(sqrt(n)) for nonnegative integers n with a lookup table."""
    global square_root_max

    # current list reaches to index (square_root_max + 1)^2 - 1
    while (square_root_max + 2) * square_root_max < n:
        square_root_max += 1
        square_root_list.extend([square_root_max] * (2 * square_root_max + 1))

    return square_root_list[n]


# Matrix utilities

def transpose(matrix):
    """Compute the transpose of a matrix."""
    return [list(row) for row in zip(*matrix)]


def determinant(matrix):
    """Compute the determinant of a square matrix recursively."""
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
    """Check that each row of a matrix has its first nonzero entry positive."""
    for row in matrix:
        if not row_is_positive(row):
            return False
    return True


def row_is_positive(row):
    """Check that a row's first nonzero entry is positive."""
    for element in row:
        if element < 0:
            return False
        elif element > 0:
            break
        elif element == 0:
            continue
    return True


def row_gcd(row):
    """Compute the gcd of a row."""
    accum = 0

    for elt in row:
        accum = gcd(accum, elt)

    return abs(accum)


def row_is_elementary(row):
    """Check whether a row is elementary (that is, a standard basis vector)."""
    zero_count = 0
    one_count = 0
    for element in row:
        if element == 0:
            zero_count += 1
        elif element == 1:
            one_count += 1

    return (zero_count == len(row) - 1) and (one_count == 1)


def rows_in_lex_order(first_row, second_row):
    """Check that a pair of rows is in decreasing lexicographic order."""
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
    """Check that the rows of a matrix are in decreasing lexicographic order."""
    for i in range(len(matrix) - 1):
        if not rows_in_lex_order(matrix[i], matrix[i + 1]):
            return False
    return True


def pretty_matrix(matrix):
    """Pretty print a matrix."""
    output = ''
    for row in matrix:
        output += pretty_matrix_row(row)
        output += '\n'

    return output


def pretty_matrix_row(row):
    output = '| '

    # TODO MAYBE: parametrize width in format
    template = "{:>3} "

    for element in row:
        output += template.format(element)

    output += '|'
    return output


# Cache good rows

# Row cache
# dictionary of dictionaries: first key is row length, second is row weight
row_cache = {}

def generate_good_rows_in_shell(length, distsquared):
    """Generate all 'good' rows (positive, non-elementary, gcd 1) for a given length and weight. Caches lists of rows for future reference."""
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
                and row_gcd(row) == 1
                and not row_is_elementary(row)
                ):
                rows.append(row)

        row_cache_for_length[distsquared] = rows

    for row in row_cache_for_length[distsquared]:
        yield row


# Lattice point enumeration

def generate_lattice_shell(n, distsquared):
    """Generate all lattice points of a given length and weight."""
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
    """Generate all normalized, non-degenerate matrices of a given size and weight."""
    if rows == 0:
        if distsquared == 0:
            yield []
    elif rows > 0:
        for i in range(distsquared):
            # first, generate rest of matrix rows
            submatrix_shell = generate_lattice_matrices_in_shell(columns, rows - 1, i)

            for submatrix in submatrix_shell:
                # now iterate through (probably cached) rows
                # distsquared - i counts down from distsquared to 1
                row_generator = generate_good_rows_in_shell(columns, distsquared - i)

                for row in row_generator:
                    if len(submatrix) == 0:
                        yield [row]
                    elif rows_in_lex_order(row, submatrix[0]):
                        yield [row] + submatrix


def generate_all_matrices(size, startweight, endweight):
    """Generate all square matrices in a range of weights."""
    for wt in range(startweight, endweight + 1):
        for mat in generate_lattice_matrices_in_shell(size, size, wt):
            yield mat


# Output formatting classes

class PrettyFormatter(object):
    """Output matrices and optional stats in a human-readable format."""
    @staticmethod
    def start_list():
        return ""

    @staticmethod
    def end_list():
        return ""

    @staticmethod
    def start_output():
        return ""

    @staticmethod
    def end_output():
        return ""

    @staticmethod
    def matrix(mat):
        return pretty_matrix(mat) + '\n'

    @staticmethod
    def stats(stats):
        lines = []

        if 'dim' in stats:
            lines.append("Matrix dimension: {}".format(stats['dim']))

        if 'det' in stats:
            lines.append("Matrix determinant: {}".format(stats['det']))

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


class ListFormatter(object):
    """Output matrices in a list, packaged in a dictionary with optional generation statistics."""
    @staticmethod
    def start_list():
        return "'matrix_list': ["

    @staticmethod
    def end_list():
        return "],"

    @staticmethod
    def start_output():
        return "{"

    @staticmethod
    def end_output():
        return "}"

    @staticmethod
    def matrix(mat):
        return '\t' + str(mat) + ',\n'

    @staticmethod
    def stats(stats):
        return "'stats': " + str(stats) + ",\n"


format_lookup = {
    'pretty': PrettyFormatter,
    'p': PrettyFormatter,
    'list': ListFormatter,
    'l': ListFormatter,
}

def print_matrix_list(dim, det, min_weight, max_weight, format, stats, max_count=0):
    """Print all valid matrices of a given size in a weight range."""
    formatter = format_lookup[format]

    count_valid = 0
    count_all = 0

    check_count = (max_count > 0)

    print formatter.start_output()
    print formatter.start_list()

    for mat in generate_all_matrices(dim, min_weight, max_weight):
        count_all += 1

        mat_det = determinant(mat)

        if (mat_det == det or mat_det == -det):
            count_valid += 1
            print formatter.matrix(transpose(mat)),

        if check_count and count_valid >= max_count:
            break

    print formatter.end_list()

    if stats:
        stat_dict = {
            'dim': dim,
            'det': det,
            'min_weight': min_weight,
            'max_weight': max_weight,
            'valid_matrix_count': count_valid,
            'generated_matrix_count': count_all,
        }

        if check_count:
            stat_dict['max_count'] = max_count

        print formatter.stats(stat_dict),

    print formatter.end_output()


# Main routine

def main(argv = None):
    """Main routine for the script."""
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Enumerates integer matrices of determinant ±1 (or ±D), ordered by
            increasing distance-squared weight.

        Normalizations and eliminations:
        * Each column starts with a positive number.
        * Columns are listed in decreasing lexicographic order.
        * The GCD of each column is 1.
        * No column is a standard basis vector.
        """))

    parser.add_argument('-n', '--dim',
        type=int,
        default=3,
        help='matrix dimension')

    parser.add_argument('-d', '--det',
        type=int,
        default=1,
        help='desired determinant of matrix')

    parser.add_argument('-a', '--min-weight',
        type=int,
        help='starting matrix weight')

    parser.add_argument('-z', '--max-weight',
        type=int,
        help='ending matrix weight')

    parser.add_argument('-c', '--max-count',
        type=int,
        default=0,
        help='maximum number of matrices to generate')

    parser.add_argument('-s', '--stats',
        action='store_true',
        help='print some stats when done')

    parser.add_argument('-f', '--format',
        choices=['pretty', 'p', 'list', 'l'],
        default='pretty',
        help='output format')
        
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s, v' + version)
                        
    args = parser.parse_args(argv[1:])

    # default to min weight of 2n + 1: should give first non-trivial matrices
    if args.min_weight is None:
        args.min_weight = 2 * args.dim + 1

    # default to max weight = min weight
    if args.max_weight is None:
        args.max_weight = args.min_weight

    print_matrix_list(**vars(args))
    

if __name__ == '__main__':
    sys.exit(main())
