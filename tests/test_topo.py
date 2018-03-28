import networkx as nx
import pandangas as pg
import pandangas.topology as top

from tests.test_core import fix_create


def test_nxgraph_creation(fix_create):
    net = fix_create
    g = top.create_nxgraph(net)
    assert type(g) == nx.MultiDiGraph
    assert len(g.nodes) == 5
    assert len(g.edges) == 5


def test_nxgraph_creation_not_in_service(fix_create):
    net = fix_create
    pg.create_pipe(net, "BUS1", "BUS2", length_m=400, diameter_m=0.02, name="OLD_PIPE", in_service=False)

    g = top.create_nxgraph(net)
    assert len(g.nodes) == 5
    assert len(g.edges) == 5

    g2 = top.create_nxgraph(net, only_in_service=False)
    assert len(g2.nodes) == 5
    assert len(g2.edges) == 6


def test_nxgraph_creation_data_nodes(fix_create):
    net = fix_create
    g = top.create_nxgraph(net)

    assert nx.get_node_attributes(g, "level")["BUS0"] == "MP"
    assert nx.get_node_attributes(g, "type")["BUS1"] == "SRCE"
    assert nx.get_node_attributes(g, "zone")["BUS2"] is None


def test_nxgraph_creation_data_edges(fix_create):
    net = fix_create
    g = top.create_nxgraph(net)

    assert nx.get_edge_attributes(g, "L_m")[("BUS1", "BUS2", 0)] == 400
    assert nx.get_edge_attributes(g, "D_m")[("BUS2", "BUS3", 0)] == 0.05
    assert nx.get_edge_attributes(g, "p_lim_kw")[("BUS0", "BUS1", 0)] == 50


def test_graphs_by_level(fix_create):
    net = fix_create
    g = top.graphs_by_level_as_dict(net)
    assert set(g.keys()).issubset(set(net.LEVELS.keys()))
    assert len(g["BP"].nodes) == 3
    assert len(g["MP"].nodes) == 2
