"""
"Median Maintenance" algorithm based on 2 heaps
given a stream of numbers keep always the median of them
"""

import argparse
import heapq

def parse_args():
    parser = argparse.ArgumentParser(description=("Input file is treated as a stream of numbers and the median "
                                                  "value when each one of them is received is accumulated (result)"))
    parser.add_argument(
        'file',
        help=('input file, one integer per row')
    )

    args = parser.parse_args()

    with open(args.file) as f:
        int_list = [int(i) for i in f.readlines()]

    return int_list


class MedianMaintainer(object):
    def __init__(self):
        self.max_heap = []
        self.min_heap = []

    def _push_3_values(self, a, b, c):
        """
        a < b < c
        """
        if len(self.max_heap) > len(self.min_heap):
            # as we only push a lower value to max_heap and the former
            # max is moved to right, we must retrieve the next max in
            # max_heap to retuen the current median
            heapq.heappush(self.max_heap, -a)
            heapq.heappush(self.min_heap, b)
            heapq.heappush(self.min_heap, c)
            median = -heapq.heappop(self.max_heap)
            heapq.heappush(self.max_heap, -median)
            return median
        else:
            heapq.heappush(self.max_heap, -a)
            heapq.heappush(self.max_heap, -b)
            heapq.heappush(self.min_heap, c)
            return b

    def push(self, value):
        """
        store a new value and return the current median
        """
        # the max value of max_heap should be the median
        try:
            max_of_left = -heapq.heappop(self.max_heap)
        except IndexError:
            max_of_left = None
        try:
            min_of_right = heapq.heappop(self.min_heap)
        except IndexError:
            min_of_right = None

        if max_of_left and min_of_right:
            # Standard case, 3 pushes to distribute
            if max_of_left < value < min_of_right:
                res = self._push_3_values(max_of_left, value, min_of_right)
            elif value < max_of_left:
                res = self._push_3_values(value, max_of_left, min_of_right)
            else:
                res = self._push_3_values(max_of_left, min_of_right, value)
            return res

        # Handle corner cases when the heaps are empty
        elif min_of_right is None and max_of_left is None:
            heapq.heappush(self.max_heap, -value)
            return value

        elif min_of_right is None:
            if value < max_of_left:
                heapq.heappush(self.max_heap, -value)
                heapq.heappush(self.min_heap, max_of_left)
                return value
            else:
                heapq.heappush(self.max_heap, -max_of_left)
                heapq.heappush(self.min_heap, value)
                return max_of_left


        else:  # max_of_left is None
            raise('ERROR this case should NEVER happen. We start filling max_heap always')


def main():
    int_list = parse_args()
    mm = MedianMaintainer()
    sum_of_medians = 0

    for i in int_list:
        sum_of_medians += mm.push(i)

    print "Total sum of medians: %s" % sum_of_medians
    print "Last 4 digits: %s" % (sum_of_medians % 10000)


if __name__ == '__main__':
    main()
