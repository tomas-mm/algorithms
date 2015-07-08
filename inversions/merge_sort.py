import sys


def merge_sort(int_list):
    l_len = len(int_list)
    if l_len < 2:
        return int_list

    elif l_len == 2:
        a, b = int_list
        if b >= a:
            return a, b
        else:
            return b, a
    else:
        p0 = merge_sort(int_list[:l_len / 2])
        p1 = merge_sort(int_list[l_len / 2:])

        i_p0 = 0
        i_p1 = 0
        res = []
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
                continue

            if b >= a:
                res.append(a)
                i_p0 += 1
            else:
                res.append(b)
                i_p1 += 1

        return res


def main(int_list):
    res = merge_sort(int_list)
    int_list.sort()
    res_ok = 'The result is correct' if res == int_list else 'Wrong result'
    print 'result: %s' % res
    print res_ok


if __name__ == '__main__':
    int_list = [int(i) for i in sys.argv[1:]]
    main(int_list)
