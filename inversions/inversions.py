import sys


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


if __name__ == '__main__':
    int_list = [int(i) for i in sys.argv[1:]]
    main(int_list)
