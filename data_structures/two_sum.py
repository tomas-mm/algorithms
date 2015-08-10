"""
Given an unsorted array A of integers and a target sum t, determine
whether or not there are 2 numbers x,y in A such x+y=t
"""

import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser(description=("Given an unsorted array A of integers and "
                                                  "a target sum t, determine whether or not "
                                                  "there are 2 numbers x,y in A such x+y=t"))

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-f', '--file',
        help=('input file, if supplied, compute the number of '
              'target values t in the interval [-10000,10000] '
              '(inclusive) such that there are distinct numbers '
              'x,y in the input file that satisfy x+y=t.')
    )

    group.add_argument(
        '-a', '--array',
        help='comma-separated list of integers in unsorted array A'
    )

    parser.add_argument(
        '-t', '--target', type=int,
        help='target value, ignored if f supplied'
    )

    args = parser.parse_args()

    if args.array:
        int_set = set(int(i) for i in args.array.split(','))
    else:
        with open(args.file) as f:
            int_set = set(int(i) for i in f.readlines())
            print 'data loaded'

    return args.target, int_set, args.file


def two_sum(target, int_set, sorted_list):
    """
    Given an unsorted array (set) A of integers and
    a target sum t, determine whether or not
    there are 2 numbers x,y in A such x+y=t
    """
    max_to_check = target / 2 + 1
    for i in sorted_list:
        if i > max_to_check:
            # as we traverse the keys in sorted order, up to this point 2 unvisited keys > target
            break

        to_find = target - i
        # ensure distinctness:
        if to_find == i:
            continue
        if to_find in int_set:
            return True, i, to_find

    return False, None, None


def main():
    t, int_set, f = parse_args()
    sorted_list = sorted(int_set)
    if not f:
        found, x, y = two_sum(t, int_set, sorted_list)
        if found:
            print "Found %s + %s = %s" % (x, y, t)

        else:
            print "Could not find any pair matching the target sum %s" % t

    else:
        count = 0
        start_time = time.time()
        for i in xrange(-10000, 10001):
            if not i % 100:
                progress = float(i + 10000) / 20000 * 100
                try:
                    remaining_time = (time.time() - start_time) * 100 / progress
                except:
                    remaining_time = None
                print 'Progress :  %s %%. Remaining time: %s' % (progress, remaining_time)
            found, x, y = two_sum(i, int_set, sorted_list)
            if found:
                count += 1
        print ("Found %s target values that can be generated as "
               "the sum of 2 distinct elements of the array") % count


if __name__ == '__main__':
    main()
