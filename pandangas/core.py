import pandas as pd
import logging


class _Network:
    def __init__(self):

        self.levels = ["HP", "MP", "BP+", "BP"]

        self.bus = pd.DataFrame(columns=["name", "level", "zone", "in_service"])
        self.pipe = pd.DataFrame(columns=["name", "from_bus", "to_bus", "length_m", "diameter_m", "in_service"])
        self.load = pd.DataFrame(columns=["name", "bus", "p_kw", "min_p_bar", "scaling"])
        self.feeder = pd.DataFrame(columns=["name", "bus", "p_lim_kw", "p_bar"])
        self.station = pd.DataFrame(columns=["name", "bus_high", "bus_low", "p_lim_kw", "p_bar"])


def _try_existing_bus(net, bus):
    """
    Check if a bus exist on a given network, raise ValueError and log an error if not

    :param net: the given network
    :param bus: the bus to check existence
    :return:
    """
    try:
        assert bus in net.bus.name.unique()
    except AssertionError:
        msg = "The bus {} does not exist !".format(bus)
        logging.error(msg)
        raise ValueError(msg)


def _check_level(net, bus_a, bus_b, same=True):
    """
    Check the pressure level of two buses on a given network, raise ValueError and log an error depending on parameter

    :param net: the given network
    :param bus_a: the first bus
    :param bus_b: the second bus
    :param same: if True, the method will check if the node have the same pressure level
    if False, the method will check if the node have different pressure levels (default: True)
    :return:
    """
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
    """
    Create an empty network

    :return: a Network object that will later contain all the buses, pipes, etc.
    """
    return _Network()


def create_bus(net, level, name, zone=None, in_service=True):
    """
    Create a bus on a given network

    :param net: the given network
    :param level: nominal pressure level of the bus
    :param name: name of the bus
    :param zone: zone of the bus (default: None)
    :param in_service: if False, the simulation will not take this bus into account (default: True)
    :return: name of the bus
    """
    try:
        assert level in net.levels
    except AssertionError:
        msg = "The pressure level of the bus {} is not in {}".format(name, net.levels)
        logging.error(msg)
        raise ValueError(msg)

    idx = len(net.bus.index)
    net.bus.loc[idx] = [name, level, zone, in_service]
    return name


def create_pipe(net, from_bus, to_bus, length_m, diameter_m, name, in_service=True):
    """
    Create a pipe between two existing buses on a given network

    :param net: the given network
    :param from_bus: the name of the already existing bus where the pipe starts
    :param to_bus: the name of the already existing bus where the pipe ends
    :param length_m: length of the pipe (in [m])
    :param diameter_m: diameter of the pipe (in [m])
    :param name: name of the pipe
    :param in_service: if False, the simulation will not take this pipe into account (default: True)
    :return: name of the pipe
    """
    _try_existing_bus(net, from_bus)
    _try_existing_bus(net, to_bus)
    _check_level(net, from_bus, to_bus)

    idx = len(net.pipe.index)
    net.pipe.loc[idx] = [name, from_bus, to_bus, length_m, diameter_m, in_service]
    return name


def create_load(net, bus, p_kw, name, min_p_bar=0.022, scaling=1.0):
    """
    Create a load attached to an existing bus in a given network

    :param net: the given network
    :param bus: the existing bus
    :param p_kw: power consumed by the load (in [kW])
    :param name: name of the load
    :param min_p_bar: minimum acceptable pressure
    :param scaling: scaling factor for the load (default: 1.0)
    :return: name of the load
    """
    _try_existing_bus(net, bus)

    idx = len(net.load.index)
    net.load.loc[idx] = [name, bus, p_kw, min_p_bar, scaling]
    return name


def create_feeder(net, bus, p_lim_kw, p_bar, name):
    """
    Create a feeder attached to an existing bus in a given network

    :param net: the given network
    :param bus: the existing bus
    :param p_lim_kw: maximum power flowing through the feeder
    :param p_bar: operating pressure level at the output of the feeder
    :param name: name of the feeder
    :return: name of the feeder
    """
    _try_existing_bus(net, bus)

    idx = len(net.feeder.index)
    net.feeder.loc[idx] = [name, bus, p_lim_kw, p_bar]
    return name


def create_station(net, bus_high, bus_low, p_lim_kw, p_bar, name):
    """
    Create a pressure station between two existing buses on different pressure level in a given network

    :param net: the given network
    :param bus_high: the existing bus with higher nominal pressure
    :param bus_low: the existing bus with lower nominal pressure
    :param p_lim_kw: maximum power flowing through the feeder
    :param p_bar: operating pressure level at the output of the feeder
    :param name: name of the station
    :return: name of the station
    """
    _try_existing_bus(net, bus_high)
    _try_existing_bus(net, bus_low)
    _check_level(net, bus_high, bus_low, same=False)

    idx = len(net.station.index)
    net.station.loc[idx] = [name, bus_high, bus_low, p_lim_kw, p_bar]
    return name
