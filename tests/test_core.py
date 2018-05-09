import pytest

import pandangas as pg


@pytest.fixture()
def fix_create():
    net = pg.create_empty_network()

    busf = pg.create_bus(net, level="MP", name="BUSF")
    bus0 = pg.create_bus(net, level="MP", name="BUS0")

    bus1 = pg.create_bus(net, level="BP", name="BUS1")
    bus2 = pg.create_bus(net, level="BP", name="BUS2")
    bus3 = pg.create_bus(net, level="BP", name="BUS3")

    pg.create_load(net, bus2, p_kW=10.0, name="LOAD2")
    pg.create_load(net, bus3, p_kW=15.0, name="LOAD3")

    pg.create_pipe(net, busf, bus0, length_m=100, diameter_m=0.05, name="PIPE0")
    pg.create_pipe(net, bus1, bus2, length_m=400, diameter_m=0.05, name="PIPE1")
    pg.create_pipe(net, bus1, bus3, length_m=500, diameter_m=0.05, name="PIPE2")
    pg.create_pipe(net, bus2, bus3, length_m=500, diameter_m=0.05, name="PIPE3")

    # TODO: switch to absolute pressure (Pa)

    pg.create_station(net, bus0, bus1, p_lim_kW=50, p_Pa=0.025E5, name="STATION")
    pg.create_feeder(net, busf, p_lim_kW=50, p_Pa=0.9E5, name="FEEDER")

    return net


def test_len_of_created_df(fix_create):
    net = fix_create
    assert len(net.bus.index) == 5
    assert len(net.pipe.index) == 4
    assert len(net.load.index) == 2
    assert len(net.feeder.index) == 1
    assert len(net.station.index) == 1


def test_columns_of_created_df(fix_create):
    net = fix_create
    assert set(net.bus.columns) == {"name", "level", "zone", "type"}
    assert set(net.pipe.columns) == {"name", "from_bus", "to_bus", "length_m", "diameter_m", "material", "in_service"}
    assert set(net.load.columns) == {"name", "bus", "p_kW", "min_p_Pa", "scaling"}
    assert set(net.feeder.columns) == {"name", "bus", "p_lim_kW", "p_Pa"}
    assert set(net.station.columns) == {"name", "bus_high", "bus_low", "p_lim_kW", "p_Pa"}


def test_bus_creation_bad_bus_level_raise_exception(fix_create):
    net = fix_create
    with pytest.raises(ValueError) as e_info:
        pg.create_bus(net, level="XX", name="BUSX")
        msg = "The pressure level of the bus BUSX is not in {}".format(["HP", "MP", "BP+", "BP"])
        assert e_info.value.message == msg
    assert len(net.bus.index) == 5


def test_pipe_creation_non_existing_bus_raise_exception(fix_create):
    net = fix_create
    with pytest.raises(ValueError) as e_info:
        pg.create_pipe(net, "BUS1", "BUSX", length_m=100, diameter_m=0.05, name="PIPEX")
        msg = "The bus {} does not exist !".format("BUSX")
        assert e_info.value.message == msg
    assert len(net.pipe.index) == 4


def test_pipe_creation_different_levels_raise_exception(fix_create):
    net = fix_create
    with pytest.raises(ValueError) as e_info:
        pg.create_pipe(net, "BUS0", "BUS1", length_m=100, diameter_m=0.05, name="PIPEX")
        msg = "The buses BUS0 and BUS1 have a different pressure level !"
        assert e_info.value.message == msg
    assert len(net.pipe.index) == 4


def test_station_creation_same_level_raise_exception(fix_create):
    net = fix_create
    with pytest.raises(ValueError) as e_info:
        pg.create_station(net, "BUS2", "BUS3", p_lim_kW=50, p_Pa=0.025E5, name="STATION")
        msg = "The buses BUS2 and BUS3 have the same pressure level !"
        assert e_info.value.message == msg
    assert len(net.station.index) == 1


def test_network_repr(fix_create):
    net = fix_create
    assert "This pandangas network includes the following parameter tables:" in repr(net)
    assert "- bus (5 elements)" in repr(net)
    assert "and the following results tables:" not in repr(net)
