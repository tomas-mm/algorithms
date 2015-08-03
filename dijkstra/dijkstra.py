"""
Find Shortest Path from a node to another using Dijkstra's Shortest-Path algorithm
"""


import argparse
import heapq


NO_PATH_DIST = 1000000


def dijkstra(edges, verts, s):
    """
    Dijkstra's Shortest-Path algorithm implementation (using heap)
    """
    x = set([s])
    all_verts = len(verts)

    # init costs with V-X vertices
    costs = [(edges[e][2], edges[e][0] if edges[e][0] != s else edges[e][1]) for e in verts[s]]
    heapq.heapify(costs)

    costs_dict = dict((vertex, cost) for cost, vertex in costs)

    while len(x) < all_verts:
        # get next vert (the one with least cost)
        try:
            v_cost, v = heapq.heappop(costs)
        except IndexError:
            print 'warning there are remaining unconnected vertices'
            break
        x.add(v)

        # update costs with edges of vertex v
        for edge in verts[v]:
            v1, v2, cost = edges[edge]
            # undirected graph
            dest = v1 if v1 != v else v2

            if dest not in x:
                current_cost = costs_dict.get(dest, NO_PATH_DIST)
                new_cost = v_cost + cost
                if new_cost < current_cost:
                    try:
                        costs.remove((current_cost, dest))
                    except ValueError:
                        pass
                    heapq.heappush(costs, (new_cost, dest))
                    costs_dict[dest] = new_cost

    return costs_dict

def parse_args():
    parser = argparse.ArgumentParser(description=("Run Dijkstra's shortest-path algorithm on a graph, "
                                                  "using s as the source vertex, and to compute the "
                                                  "shortest-path distances between s and every other "
                                                  "vertex of the graph. If there is no path between a "
                                                  "vertex v and vertex s, we'll define the shortest-path "
                                                  "distance between s and v to be %s. " % NO_PATH_DIST))

    parser.add_argument(
        '--file', '-f',
        required=True,
        help=('Each row consists of the node tuples that are adjacent to that particular vertex (undirected) '
              'along with the length of that edge. For example, the 6th row has 6 as the first entry indicating '
              'that this row corresponds to the vertex labeled 6. The next entry of this row "141,8200" indicates '
              'that there is an edge between vertex 6 and vertex 141 that has length 8200. The rest of the pairs '
              'of this row indicate the other vertices adjacent to vertex 6 and the lengths of the corresponding '
              'edges.')
    )

    parser.add_argument('--source', '-s', default=1, type=int,
                        help='Source vertex s to compute shortest paths from [default: %(default)s]')
    parser.add_argument('--report', '-r', default='7,37,59,82,99,115,133,165,188,197',
                        help=('comma-separated list of vertices (integers) to report '
                              'shortest-path distances to [default: %(default)s]'))

    args = parser.parse_args()

    return args


def get_adjacency_lists_with_costs(in_file):
    edges = {}
    verts = {}
    edge_count = 0
    with open(in_file) as f:
        for line in f:
            vertex = line.split()
            v1 = int(vertex[0])
            for v2_s in vertex[1:]:
                v2_sn, v2_sc = v2_s.split(',')
                v2 = int(v2_sn)
                v2_c = int(v2_sc)
                if v2 > v1:
                    # avoid adding duplicated edges in the loaded graph (undirected)
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

                edges[edge_count] = [v1, v2, v2_c]
                edge_count += 1

    return edges, verts


if __name__ == '__main__':
    args = parse_args()
    edges, verts = get_adjacency_lists_with_costs(args.file)

    costs = dijkstra(edges, verts, args.source)

    paths_to_print = [int(i.strip()) for i in args.report.strip().split(',')]
    print "Paths required: %s" % ','.join([str(i) for i in paths_to_print])

    costs_to_print = [costs.get(i, NO_PATH_DIST) for i in paths_to_print]
    print "Costs of paths required: %s" % ','.join([str(i) for i in costs_to_print])
