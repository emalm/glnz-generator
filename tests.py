#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime

from glnzlist import *

print version

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

            # for row in mat:
            #     print row_gcd(row)

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
        'length': 4,
        'start': 1,
        'stop': 12,
        'print_matrices': False
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


if __name__ == '__main__':
    sys.exit(test_suite())
