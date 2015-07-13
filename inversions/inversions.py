import argparse


def merge_sort_and_count_inversions(int_list):
    l_len = len(int_list)
    if l_len < 2:
        return int_list, 0

    elif l_len == 2:
        a, b = int_list
        if b >= a:
            return [a, b], 0
        else:
            return [b, a], 1
    else:
        p0, c0 = merge_sort_and_count_inversions(int_list[:l_len / 2])
        p1, c1 = merge_sort_and_count_inversions(int_list[l_len / 2:])

        i_p0 = 0
        i_p1 = 0
        res = []
        c_split = 0
        for _i in range(l_len):
            try:
                a = p0[i_p0]
            except IndexError:
                res.append(p1[i_p1])
                i_p1 += 1
                continue

            try:
                b = p1[i_p1]
            except IndexError:
                res.append(p0[i_p0])
                i_p0 += 1
                # counting c_split here in the opposite way will count inversions twice
                continue

            if b >= a:
                res.append(a)
                i_p0 += 1
            else:
                res.append(b)
                i_p1 += 1
                remaining_in_p0 = len(p0) - i_p0
                c_split += remaining_in_p0

        return res, c0 + c1 + c_split


def main(int_list):
    res, count = merge_sort_and_count_inversions(int_list)
    int_list.sort()
    res_ok = 'The sorted result is correct' if res == int_list else 'Wrong result'

    print 'Sorted result: %s' % res
    print res_ok

    print 'Number of inversions: %s' % count


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
