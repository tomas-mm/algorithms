import copy
import random
import argparse


number_of_comparisons = 0


def choose_pivot(int_list, sort_range):
    """
    Configure different pivot choice algorithms
    """
    # return choose_pivot_random(int_list, sort_range)
    # return choose_pivot_first(int_list, sort_range)
    # return choose_pivot_last(int_list, sort_range)
    return choose_pivot_median_of_3(int_list, sort_range)
    # return choose_pivot_median_of_3_isort(int_list, sort_range)
    # return choose_pivot_median_of_3_bf(int_list, sort_range)


def choose_pivot_first(int_list, sort_range):
    """
    Fixed pivot choice (first element)
    """
    pos = sort_range[0]
    return pos


def choose_pivot_last(int_list, sort_range):
    """
    Fixed pivot choice (last element)
    """
    pos = sort_range[1] - 1
    return pos


def choose_pivot_median_of_3_bf(int_list, sort_range):
    """
    "Median-of-three" pivot rule (brute force comparisons)
    """
    m = sort_range[1] - sort_range[0]
    first_pos = sort_range[0]
    last_pos = sort_range[1] - 1
    mid_pos = first_pos + (m - 1) / 2

    if (int_list[first_pos] <= int_list[mid_pos] <= int_list[last_pos]
        or
        int_list[last_pos] <= int_list[mid_pos] <= int_list[first_pos]):
        p = mid_pos
    elif (int_list[mid_pos] <= int_list[first_pos] <= int_list[last_pos]
          or
          int_list[last_pos] <= int_list[first_pos] <= int_list[mid_pos]):
        p = first_pos
    else:
        p = last_pos

    return p


# several implementations of the median pivot choice

def choose_pivot_median_of_3(int_list, sort_range):
    """
    "Median-of-three" pivot rule
    """
    m = sort_range[1] - sort_range[0]

    first_pos = sort_range[0]
    last_pos = sort_range[1] - 1
    mid_pos = first_pos + (m - 1) / 2

    # merge sort style
    pos_list = [first_pos, mid_pos, last_pos]
    if int_list[pos_list[0]] > int_list[pos_list[1]]:
        pos_list = [pos_list[1], pos_list[0], pos_list[2]]
    if int_list[pos_list[2]] >= int_list[pos_list[1]]:
        p = pos_list[1]
    elif int_list[pos_list[2]] <= int_list[pos_list[0]]:
        p = pos_list[0]
    else:
        p = pos_list[2]

    # debug
    correct = [first_pos, mid_pos, last_pos]
    correct.sort(key=lambda x: int_list[x])
    if p != correct[1]:
        print 'Alert!!'

    return p


def choose_pivot_median_of_3_isort(int_list, sort_range):
    """
    "Median-of-three" pivot rule
    """
    m = sort_range[1] - sort_range[0]
    first_pos = sort_range[0]
    last_pos = sort_range[1] - 1
    mid_pos = first_pos + (m - 1) / 2

    # using insertion sort
    pos_list = [first_pos, mid_pos, last_pos]
    insertion_sort(pos_list, comp=lambda x: int_list[x])
    p = pos_list[1]

    return p


def insertion_sort(int_list, comp=None):
    """
    Insertion sort implementation. Modifies the input list in-place.
    """
    if not comp:
        comp = lambda x: x

    for i in range(1, len(int_list)):
        x = int_list[i]
        j = i
        while j > 0 and comp(int_list[j - 1]) > comp(x):
            int_list[j] = int_list[j - 1]
            j = j - 1
        int_list[j] = x


def choose_pivot_random(int_list, sort_range):
    """
    Ramdom pivot choice
    """
    pos = random.randrange(*sort_range)
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

    new_pos = greater_than_pivot_pointer - 1

    if sort_range[0] != new_pos:
        swap_pos(int_list, sort_range[0], greater_than_pivot_pointer - 1)

    return new_pos


def quick_sort(int_list, sort_range=None):
    if not sort_range:
        sort_range = (0, len(int_list))

    m = sort_range[1] - sort_range[0]

    if m < 2:
        return

    # exercise probe
    global number_of_comparisons
    number_of_comparisons += (m - 1)

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

    print 'Sorted result (truncated to 100): %s' % res[:100]
    print res_ok

    print 'number of comparisons: %s' % number_of_comparisons


def get_int_list_from_args():
    parser = argparse.ArgumentParser(description=('Quick sort implementation. '
                                                  'Reports the number of comparisons used.'))

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
