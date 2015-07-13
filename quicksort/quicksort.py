import copy
import argparse


def choose_pivot(int_list, sort_range):
    """
    Fixed pivot choosing
    """
    pos = sort_range[0]
    return int_list[pos], pos


def partition(int_list, sort_range, pivot, pos):
    """
    NOT minimal memory implementation
    modifies int_list and returns the new position of the pivot
    """
    prev = []
    post = []
    middle = []
    for i in range(*sort_range):
        a = int_list[i]
        if a < pivot:
            prev.append(a)
        elif a > pivot:
            post.append(a)
        else:
            middle.append(a)

    res = prev + middle + post
    new_pos = len(prev) + 1

    # partially rewrite int_list
    int_list[sort_range[0]:sort_range[1]] = res

    return new_pos


def quick_sort(int_list, sort_range=None):
    if not sort_range:
        sort_range = (0, len(int_list))

    if len(int_list[sort_range[0]:sort_range[1]]) < 2:
        return

    else:
        piv, p = choose_pivot(int_list, sort_range)

        new_pos = partition(int_list, sort_range, piv, p)

        quick_sort(int_list, sort_range=(sort_range[0], new_pos))
        quick_sort(int_list, sort_range=(new_pos + 1, sort_range[1]))


def main(int_list):
    res = copy.deepcopy(int_list)
    quick_sort(res)
    int_list.sort()
    res_ok = 'The sorted result is correct' if res == int_list else 'Wrong result'

    print 'Sorted result: %s' % res
    print res_ok


def get_int_list_from_args():
    parser = argparse.ArgumentParser(description='Count inversions in an integer array.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--integers', '-i', help='comma-separated list of integers')
    group.add_argument('--file', '-f', help='file with a list of integers (one per line)')

    args = parser.parse_args()

    if args.integers:
        int_list = [int(i) for i in args.integers.split(',')]
    else:
        with open(args.file) as f:
            int_list = [int(i) for i in f.readlines()]

    return int_list


if __name__ == '__main__':
    int_list = get_int_list_from_args()
    main(int_list)
