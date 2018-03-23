import networkx as nx


def create_nxgraph(net, only_in_service=True):
    """
    Convert a given network into a NetworkX MultiGraph

    :param net: the given network
    :param only_in_service: if True, convert only the pipes that are in service (default: True)
    :return: a MultiGraph
    """

    g = nx.MultiDiGraph()

    for idx, row in net.bus.iterrows():
        g.add_node(row[0], index=idx, level=row[1], zone=row[2], type=row[3])

    pipes = net.pipe
    if only_in_service:
        pipes = pipes.loc[pipes["in_service"] != False]

    for idx, row in pipes.iterrows():
        g.add_edge(row[1], row[2], name=row[0], index=idx, length_m=row[3], diameter=row[4], edge_type="PIPE")

    return g
