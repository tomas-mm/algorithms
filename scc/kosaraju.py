"""
Find Strongly Connected Components (SCCs) of a directed graph using
Kosaraju's 2-pass algorithm
"""


import argparse


def dfs(edges, verts, new_verts_order, explored_verts,
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


    for e in verts[i]:
        arc = list(edges[e])
        if reverse:
            arc.reverse()
        if arc[0] == i:
            # outgoing arc
            if arc[1] not in explored_verts:
                dfs(edges, verts, new_verts_order, explored_verts,
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
        for line in f.readlines():
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
    sections = scc(edges, verts)

    print "Strongly Connected Sections: %s" % sections
    print "Number of Strongly Connected Sections: %s" % len(sections)

