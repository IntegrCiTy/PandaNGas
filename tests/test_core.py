import pytest

import pandangas as pg


@pytest.fixture()
def fix_create():
    net = pg.create_empty_network()

    bus0 = pg.create_bus(net, level="MP", name="BUS0")

    bus1 = pg.create_bus(net, level="BP", name="BUS1")
    bus2 = pg.create_bus(net, level="BP", name="BUS2")
    bus3 = pg.create_bus(net, level="BP", name="BUS3")

    pg.create_load(net, bus2, p_kw=10.0, name="LOAD2")
    pg.create_load(net, bus2, p_kw=13.0, name="LOAD3")

    pg.create_pipe(net, bus1, bus2, length_m=100, diameter_m=0.05, name="PIPE1")
    pg.create_pipe(net, bus1, bus3, length_m=200, diameter_m=0.05, name="PIPE2")

    pg.create_station(net, bus0, bus1, p_lim_kw=50, p_bar=0.022, name="STATION")
    pg.create_feeder(net, bus0, p_lim_kw=50, p_bar=4.5, name="FEEDER")

    return net


def test_len_of_created_df(fix_create):
    net = fix_create
    assert len(net.bus.index) == 4
    assert len(net.pipe.index) == 2
    assert len(net.load.index) == 2
    assert len(net.feeder.index) == 1
    assert len(net.station.index) == 1
