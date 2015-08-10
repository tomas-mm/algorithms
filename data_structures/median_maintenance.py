"""
"Median Maintenance" algorithm based on 2 heaps
given a stream of numbers keep always the median
of them when a new one is added.
"""

import argparse
import heapq


def parse_args():
    parser = argparse.ArgumentParser(
        description=("Input file is treated as a stream of numbers and the median "
                     "value when each one of them is received is accumulated (result)")
    )
    parser.add_argument(
        'file',
        help=('input file, one integer per row')
    )

    args = parser.parse_args()

    with open(args.file) as f:
        int_list = [int(i) for i in f.readlines()]

    return int_list


class MedianMaintainer(object):
    """
    Class to maintain the median of a stream of numbers using two heaps
    """
    def __init__(self):
        self.max_heap = []
        self.min_heap = []

    def push(self, value):
        """
        store a new value and return the current median
        """

        l_max = len(self.max_heap)
        l_min = len(self.min_heap)

        try:
            max_of_left = -self.max_heap[0]
            min_of_right = self.min_heap[0]
        except IndexError:
            # Handle initialization cases with both heaps empty or min_heap only empty
            if  l_max == 0:
                heapq.heappush(self.max_heap, -value)
                return value

            if l_min == 0:
                max_of_left = -heapq.heappop(self.max_heap)
                if value > max_of_left:
                    heapq.heappush(self.max_heap, -max_of_left)
                    heapq.heappush(self.min_heap, value)
                    return max_of_left
                else:
                    heapq.heappush(self.max_heap, -value)
                    heapq.heappush(self.min_heap, max_of_left)
                    return value

        if l_max == l_min:
            if value <= min_of_right:
                heapq.heappush(self.max_heap, -value)
            else:
                min_of_right = heapq.heappop(self.min_heap)
                heapq.heappush(self.min_heap, value)
                heapq.heappush(self.max_heap, -min_of_right)
        else:
            # l_max > l_min
            if value >= min_of_right:
                heapq.heappush(self.min_heap, value)
            else:
                heapq.heappush(self.max_heap, -value)
                max_of_left = -heapq.heappop(self.max_heap)
                heapq.heappush(self.min_heap, max_of_left)

        return -self.max_heap[0]


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
