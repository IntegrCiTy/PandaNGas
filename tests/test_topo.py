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
