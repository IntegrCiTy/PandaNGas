import networkx as nx


def create_nxgraph(net, only_in_service=True):
    """
    Convert a given network into a NetworkX MultiGraph

    :param net: the given network
    :param only_in_service: if True, convert only the pipes that are in service (default: True)
    :return: a MultiGraph
    """

    g = nx.MultiGraph()

    for idx, row in net.bus.iterrows():
        g.add_node(row[0], index=idx, level=row[1], zone=row[2])

    pipes = net.pipe
    print(pipes)
    if only_in_service:
        pipes = pipes.loc[pipes["in_service"] != False]
        print(pipes)

    for idx, row in pipes.iterrows():
        g.add_edge(row[1], row[2], name=row[0], index=idx, length_m=row[3], diameter=row[4], edge_type="PIPE")

    for idx, row in net.station.iterrows():
        g.add_edge(row[1], row[2], name=row[0], index=idx, p_lim_kw=row[3], p_bar=row[4], edge_type="STATION")

    return g
