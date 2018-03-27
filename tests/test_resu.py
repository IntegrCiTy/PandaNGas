import pandangas as pg
import pandangas.simulation as sim
import pandangas.results as res

from tests.test_core import fix_create


def test_runpp(fix_create):
    net = fix_create
    res.runpp(net)
    assert len(net.res_bus.index) == 3