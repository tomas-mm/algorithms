"""
Find Strongly Connected Components (SCCs) of a directed graph using
Kosaraju's 2-pass algorithm
"""


import sys
import argparse
import random


def dfs(edges, verts, new_verts_order, explored_verts,
        sections, leader, i, reverse=False):
    """
    Depth-First Search from vertex i (non-recursive implementation)
    Recursive implementation would fail for big data sets on systems with
    limited memory (even increasing the recursion limit)
    Modifies new_verts_order, explored_verts and sections
    """
    execution_stack = [i]

    while len(execution_stack) > 0:
        v = execution_stack.pop()

        if isinstance(v, tuple):
            # finish mark
            new_verts_order.append(v[0])
        else:
            if v in explored_verts:  # we reached here through another path before
                continue

            # set leader and mark as explored
            explored_verts[v] = leader
            try:
                sections[leader].append(v)
            except KeyError:
                sections[leader] = [v]

            # debug
            if random.randint(1, 100) == 1:
                l_explored = len(explored_verts)
                l_verts = len(verts)
                print "Explored %s of %s (%s%%)" % (l_explored, l_verts, float(l_explored) / l_verts * 100)

            execution_stack.append((v,))  # finish mark

            for e in verts[v]:
                arc = list(edges[e])
                if reverse:
                    arc.reverse()
                if arc[0] == v:
                    # outgoing arc
                    if arc[1] not in explored_verts:
                        execution_stack.append(arc[1])


def dfs_recursive(edges, verts, new_verts_order, explored_verts,
        sections, leader, i, reverse=False):
    """
    Depth-First Search from vertex i
    Modifies new_verts_order, explored_verts and sections
    """
    # set leader and mark as explored
    explored_verts[i] = leader
    try:
        sections[leader].append(i)
    except KeyError:
        sections[leader] = [i]

    # debug
    if random.randint(1, 100) == 1:
        l_explored = len(explored_verts)
        l_verts = len(verts)
        print "Explored %s of %s (%s%%)" % (l_explored, l_verts, float(l_explored) / l_verts * 100)

    for e in verts[i]:
        arc = list(edges[e])
        if reverse:
            arc.reverse()
        if arc[0] == i:
            # outgoing arc
            if arc[1] not in explored_verts:
                dfs_recursive(edges, verts, new_verts_order, explored_verts,
                    sections, leader, arc[1], reverse)

    new_verts_order.append(i)


def dfs_loop(edges, verts, verts_order, reverse=False):
    """
    Depth-First Search Loop
    Returns:
        - new vertex order according to finishing times (the position
        of a vertex in the list is its finishing time)
        - dictionary of sections
    """
    new_verts_order = []
    sections = {}
    explored_verts = {}

    for s in reversed(verts_order):
        if s not in explored_verts:
            # dfs_recursive(edges, verts, new_verts_order, explored_verts,
            #              sections, s, s, reverse)

            dfs(edges, verts, new_verts_order, explored_verts,
                sections, s, s, reverse)

    return new_verts_order, sections


def scc(edges, verts):
    """
    Find Strongly Connected Components (SCCs) of a directed graph using Kosaraju's 2-pass algorithm.
    Returns: dictionary of sections
    """
    verts_order = verts.keys()
    # verts_order.sort()  # debug, actually doesn't mind in the 1st pass

    new_verts_order, _ = dfs_loop(edges, verts, verts_order, reverse=True)
    _, sections = dfs_loop(edges, verts, new_verts_order, reverse=False)

    return sections


def parse_args():
    parser = argparse.ArgumentParser(description=("Find Strongly Connected Components (SCCs) of a "
                                                  "directed graph using Kosaraju's 2-pass algorithm. "
                                                  'Reports the number of SCCs'))

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


def get_adjacency_lists_directed(in_file):
    edges = {}
    verts = {}
    edge_count = 0
    with open(in_file) as f:
        for line in f:
            vertex = line.split()
            v1 = int(vertex[0])
            for v2_s in vertex[1:]:
                v2 = int(v2_s)
                # adding duplicated edges is allowed
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
    edges, verts = get_adjacency_lists_directed(args.file)

    # Use a bigger recursion limit for big data (in unix systems new system
    # ulimit would also have to be applied).
    # This seems not work in Windows (use non-recursive approach there)
    recursion_limit = max(sys.getrecursionlimit(), len(verts))
    sys.setrecursionlimit(recursion_limit)
    print 'recursion limit set to %s' % recursion_limit

    sections = scc(edges, verts)

    # getting the 5 largest sections
    section_sizes = [(k, len(v)) for k, v in sections.iteritems()]
    section_sizes.sort(key=lambda x: x[1], reverse=True)

    # print "Strongly Connected Sections: %s" % sections
    print "Number of Strongly Connected Sections: %s" % len(sections)
    print "Largest sections: %s" % section_sizes[:5]

