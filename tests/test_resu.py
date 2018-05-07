import pandangas as pg
import pandangas.simulation as sim
import pandangas.results as res

from tests.test_core import fix_create


def test_runpp(fix_create):
    net = fix_create
    res.runpp(net)
    assert len(net.res_bus.index) == 5
    idx = net.res_bus.index[net.res_bus["name"] == "BUS2"].tolist()[0]
    assert net.res_bus.at[idx, "p_Pa"] == 1962.7
