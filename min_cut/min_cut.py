"""
Karger random contraction algorithm to compute minimum cut of a graph
"""

import copy
import time
import math
import random
import argparse


random.seed()


def min_cut_basic(edges, verts):
    """
    Modifies edges and verts.
    verts will have only 2 elements, len(edges) = min cut size
    verts keys will have all the vertices in each block '_'-separated
    """
    # while more than 2 remaining vertices:
    #     get radom edge (remaining ones)
    #     contract graph
    #     remove self loops

    while len(verts) > 2:
        edge = random.choice(edges.keys())
        v1, v2 = edges[edge]

        # merge vertices into a single label
        merged_v_label = '%s_%s' % (v1, v2)
        edges_v1 = verts.pop(v1)
        edges_v2 = verts.pop(v2)
        verts[merged_v_label] = edges_v1.union(edges_v2)

        # edge and self loops -> remove
        edges_to_remove = edges_v1.intersection(edges_v2)
        verts[merged_v_label].difference_update(edges_to_remove)
        for e in edges_to_remove:
            edges.pop(e)

        # replace old vertices names in the edges
        for e in verts[merged_v_label]:
            if edges[e][0] in (v1, v2):
                edges[e][0] = merged_v_label
            else:
                edges[e][1] = merged_v_label


def min_cut(edges, verts):
    """
    Calls N times min_cut_basic keeping the best result (smallest cut)
    Returns (minimun_cut_size, min_cut)
    min cut is a list containing the two blocks (vertices are represented as a str with
     '_'-separated vertex names)
    """
    n = len(verts)
    N = int(math.ceil(math.log(n) * n * n))  # error prob = 1/n
    # N = n * n * n  # less error prob
    smallest_cut = len(edges)
    cut_verts = []

    print "first choice: %s" % random.choice(edges.keys())  # debug
    time_in_its = 0

    for i in xrange(N):
        ts = time.time()
        e = copy.deepcopy(edges)
        v = copy.deepcopy(verts)
        min_cut_basic(e, v)

        if len(e) < smallest_cut:
            smallest_cut = len(e)
            cut_verts = v.keys()
            print "\nNew min cut: %s\n" % smallest_cut

        time_in_its += time.time() - ts

        if i % n == 0:
            print "iteration %s of %s" % (i, N)
            av_time = time_in_its / (i + 1)
            print "remaining time: %s s" % (av_time * (N - i))

    return smallest_cut, cut_verts


def parse_args():
    parser = argparse.ArgumentParser(description=('Karger random contraction algorithm. '
                                                  'Reports the number of edges in the min cut.'))

    parser.add_argument(
        'file',
        help=('The first column in the file represents the vertex label, '
              'and the particular row (other entries except the first column) '
              'tells all the vertices that the vertex is adjacent to. '
              'So for example, the 6th row looks like : "6 155 56 52 120 ......". '
              'This just means that the vertex with label 6 is adjacent to '
              '(i.e., shares an edge with) the vertices with labels 155,56,52,120,......,etc')
    )

    args = parser.parse_args()

    return args


def get_adjacency_lists(in_file):
    edges = {}
    verts = {}
    edge_count = 0
    with open(in_file) as f:
        for line in f.readlines():
            vertex = line.split()
            v1 = int(vertex[0])
            for v2_s in vertex[1:]:
                v2 = int(v2_s)
                if v2 > v1:
                    # avoid adding duplicated edges in the loaded graph
                    try:
                        verts[v1].add(edge_count)  # edges in v1
                    except KeyError:
                        verts[v1] = set()
                        verts[v1].add(edge_count)
                    try:
                        verts[v2].add(edge_count)  # edges in v2
                    except KeyError:
                        verts[v2] = set()
                        verts[v2].add(edge_count)

                    edges[edge_count] = [v1, v2]
                    edge_count += 1

    return edges, verts


if __name__ == '__main__':
    args = parse_args()
    edges, verts = get_adjacency_lists(args.file)
    minimun_cut_size, mcut = min_cut(edges, verts)

    print "Min cut: %s" % mcut
    print "Min cut size: %s" % minimun_cut_size

