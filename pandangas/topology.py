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
        g.add_edge(row[1], row[2], name=row[0], index=idx, L_m=row[3], D_m=row[4], mat=row[5], type="PIPE")

    for idx, row in net.station.iterrows():
        g.add_edge(row[1], row[2], name=row[0], index=idx, p_lim_kw=row[3], p_bar=row[4], type="STATION")

    return g


def graphs_by_level_as_dict(net):
    levels = net.bus["level"].unique()
    g = create_nxgraph(net)
    g_dict = {}
    for l in levels:
        nodes = [n for n, data in g.nodes(data=True) if data["level"] == l]
        g_dict[l] = g.subgraph(nodes)
    return g_dict
