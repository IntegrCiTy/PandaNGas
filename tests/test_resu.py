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


def test_len_of_created_df(fix_create):
    net = fix_create
    res.runpp(net)
    assert len(net.res_bus.index) == 5
    assert len(net.res_pipe.index) == 4
    assert len(net.res_feeder.index) == 1
    assert len(net.res_station.index) == 1


def test_columns_of_created_df(fix_create):
    net = fix_create
    res.runpp(net)
    assert set(net.res_bus.columns) == {"name", "p_Pa"}
    assert set(net.res_pipe.columns) == {"name", "m_dot_kg/s", "v_m/s", "p_kW", "loading_percent"}
    assert set(net.res_feeder.columns) == {"name", "m_dot_kg/s", "p_kW", "loading_percent"}
    assert set(net.res_station.columns) == {"name", "m_dot_kg/s", "p_kW", "loading_percent"}
