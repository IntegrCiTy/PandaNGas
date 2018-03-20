import pandas as pd
import logging


class _Network:
    def __init__(self):

        self.levels = ["HP", "MP", "BP+", "BP"]

        self.bus = pd.DataFrame(columns=["name", "level", "zone", "in_service"])
        self.pipe = pd.DataFrame(columns=["name", "from_bus", "to_bus", "length_m", "diameter_m"])
        self.load = pd.DataFrame(columns=["name", "bus", "p_kw", "scaling"])
        self.feeder = pd.DataFrame(columns=["name", "bus", "p_lim_kw", "p_bar"])
        self.station = pd.DataFrame(columns=["name", "bus_high", "bus_low", "p_lim_kw", "p_bar"])


def _try_existing_bus(net, bus):
    try:
        assert bus in net.bus.name.unique()
    except AssertionError:
        msg = "The bus {} does not exist !".format(bus)
        logging.error(msg)
        raise ValueError(msg)


def _check_level(net, bus_a, bus_b, same=True):
    lev_a = net.bus.loc[net.bus.name == bus_a, "level"].all()
    lev_b = net.bus.loc[net.bus.name == bus_b, "level"].all()
    if same:
        try:
            assert lev_a == lev_b
        except AssertionError:
            msg = "The buses {} and {} have a different pressure level !".format(bus_a, bus_b)
            logging.error(msg)
            raise ValueError(msg)
    else:
        try:
            assert lev_a != lev_b
        except AssertionError:
            msg = "The buses {} and {} have the same pressure level !".format(bus_a, bus_b)
            logging.error(msg)
            raise ValueError(msg)


def create_empty_network():
    return _Network()


def create_bus(net, level, name, zone=None, in_service=True):
    try:
        assert level in net.levels
    except AssertionError:
        msg = "The pressure level of the bus {} is not in {}".format(name, net.levels)
        logging.error(msg)
        raise ValueError(msg)

    idx = len(net.bus.index)
    net.bus.loc[idx] = [name, level, zone, in_service]
    return name


def create_pipe(net, from_bus, to_bus, length_m, diameter_m, name):
    _try_existing_bus(net, from_bus)
    _try_existing_bus(net, to_bus)
    _check_level(net, from_bus, to_bus)

    idx = len(net.pipe.index)
    net.pipe.loc[idx] = [name, from_bus, to_bus, length_m, diameter_m]
    return name


def create_load(net, bus, p_kw, name, scaling=1.0):
    _try_existing_bus(net, bus)

    idx = len(net.load.index)
    net.load.loc[idx] = [name, bus, p_kw, scaling]
    return name


def create_feeder(net, bus, p_lim_kw, p_bar, name):
    _try_existing_bus(net, bus)

    idx = len(net.feeder.index)
    net.feeder.loc[idx] = [name, bus, p_lim_kw, p_bar]
    return name


def create_station(net, bus_high, bus_low, p_lim_kw, p_bar, name):
    _try_existing_bus(net, bus_high)
    _try_existing_bus(net, bus_low)
    _check_level(net, bus_high, bus_low, same=False)

    idx = len(net.station.index)
    net.station.loc[idx] = [name, bus_high, bus_low, p_lim_kw, p_bar]
    return name
