import networkx as nx
import pandangas as pg
import pandangas.topology as top

from tests.test_core import fix_create


def test_nxgraph_creation(fix_create):
    net = fix_create
    g = top.create_nxgraph(net)
    assert type(g) == nx.MultiGraph
    assert len(g.nodes) == 4
    assert len(g.edges) == 3


def test_nxgraph_creation_not_in_service(fix_create):
    net = fix_create
    pg.create_pipe(net, "BUS2", "BUS3", length_m=100, diameter_m=0.05, name="OLD_PIPE", in_service=False)

    g = top.create_nxgraph(net)
    assert type(g) == nx.MultiGraph
    assert len(g.nodes) == 4
    assert len(g.edges) == 3

    g2 = top.create_nxgraph(net, only_in_service=False)
    assert type(g2) == nx.MultiGraph
    assert len(g2.nodes) == 4
    assert len(g2.edges) == 4
