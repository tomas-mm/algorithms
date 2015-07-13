import copy
import argparse


def choose_pivot(int_list, sort_range):
    """
    Fixed pivot choosing
    """
    pos = sort_range[0]
    return pos


def partition_not_in_place(int_list, sort_range, pos):
    """
    NOT minimal memory implementation (not in-place)
    modifies int_list and returns the new position of the pivot
    """
    pivot = int_list[pos]
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
    new_pos = len(prev) + sort_range[0]

    # partially rewrite int_list
    int_list[sort_range[0]:sort_range[1]] = res

    return new_pos


def swap_pos(int_list, i, j):
    t = int_list[i]
    int_list[i] = int_list[j]
    int_list[j] = t


def partition(int_list, sort_range, pos):
    """
    In-place implementation
    modifies int_list and returns the new position of the pivot
    """
    pivot = int_list[pos]
    # preprocessing step
    if pos != sort_range[0]:
        swap_pos(int_list, sort_range[0], pos)

    unpart_pointer = sort_range[0] + 1
    greater_than_pivot_pointer = unpart_pointer

    for i in range(unpart_pointer, sort_range[1]):
        if int_list[i] < pivot:
            if greater_than_pivot_pointer < i:
                # elements bigger than the pivot have been seen
                swap_pos(int_list, i, greater_than_pivot_pointer)
            greater_than_pivot_pointer += 1

    if sort_range[0] != greater_than_pivot_pointer - 1:
        swap_pos(int_list, sort_range[0], greater_than_pivot_pointer - 1)

    return greater_than_pivot_pointer


def quick_sort(int_list, sort_range=None):
    if not sort_range:
        sort_range = (0, len(int_list))

    if len(int_list[sort_range[0]:sort_range[1]]) < 2:
        return

    else:
        piv_pos = choose_pivot(int_list, sort_range)

        new_pos = partition(int_list, sort_range, piv_pos)
        # new_pos = partition_not_in_place(int_list, sort_range, piv_pos)

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
