#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implementation of the network creation methods.

    Usage:

    >>> import pandangas as pg

    >>> net = pg.create_empty_network()

    >>> busf = pg.create_bus(net, level="MP", name="BUSF")
    >>> bus0 = pg.create_bus(net, level="MP", name="BUS0")

    >>> bus1 = pg.create_bus(net, level="BP", name="BUS1")
    >>> bus2 = pg.create_bus(net, level="BP", name="BUS2")
    >>> bus3 = pg.create_bus(net, level="BP", name="BUS3")

    >>> pg.create_load(net, bus2, p_kW=10.0, name="LOAD2")
    >>> pg.create_load(net, bus3, p_kW=13.0, name="LOAD3")

    >>> pg.create_pipe(net, busf, bus0, length_m=100, diameter_m=0.05, name="PIPE0")
    >>> pg.create_pipe(net, bus1, bus2, length_m=400, diameter_m=0.05, name="PIPE1")
    >>> pg.create_pipe(net, bus1, bus3, length_m=500, diameter_m=0.05, name="PIPE2")
    >>> pg.create_pipe(net, bus2, bus3, length_m=500, diameter_m=0.05, name="PIPE3")

    >>> pg.create_station(net, bus0, bus1, p_lim_kW=50, p_Pa=0.025E5, name="STATION")
    >>> pg.create_feeder(net, busf, p_lim_kW=50, p_Pa=0.9E5, name="FEEDER")

"""

import pandas as pd
import logging


logging.basicConfig(level=logging.DEBUG)


class _Network:

    LEVELS = {"HP": 5.0E5, "MP": 1.0E5, "BP+": 0.1E5, "BP": 0.025E5}  # Pa
    LHV = 38.1E3  # kJ/kg
    V_MAX = 2.0   # m/s

    def __init__(self):

        self.bus = pd.DataFrame(columns=["name", "level", "zone", "type"])
        self.pipe = pd.DataFrame(columns=["name", "from_bus", "to_bus", "length_m", "diameter_m", "in_service"])
        self.load = pd.DataFrame(columns=["name", "bus", "p_kW", "min_p_Pa", "scaling"])
        self.feeder = pd.DataFrame(columns=["name", "bus", "p_lim_kW", "p_Pa"])
        self.station = pd.DataFrame(columns=["name", "bus_high", "bus_low", "p_lim_kW", "p_Pa"])

        self.res_bus = pd.DataFrame(columns=["name", "p_Pa"])
        self.res_pipe = pd.DataFrame(columns=["name", "m_dot_kg/s", "v_m/s", "p_kW", "loading_percent"])
        self.res_feeder = pd.DataFrame(columns=["name", "m_dot_kg/s", "p_kW", "loading_percent"])
        self.res_station = pd.DataFrame(columns=["name", "m_dot_kg/s", "p_kW", "loading_percent"])

        self.keys = {"bus", "pipe", "load", "feeder", "station", "res_bus", "res_pipe", "res_feeder", "res_station"}

    def __repr__(self):
        r = "This pandangas network includes the following parameter tables:"
        par = []
        res = []
        for tb in self.keys:
            if len(getattr(self, tb)) > 0:
                if 'res_' in tb:
                    res.append(tb)
                else:
                    par.append(tb)
        for tb in par:
            length = len(getattr(self, tb))
            r += "\n   - %s (%s %s)" % (tb, length, "elements" if length > 1 else "element")
        if res:
            r += "\n and the following results tables:"
            for tb in res:
                length = len(getattr(self, tb))
                r += "\n   - %s (%s %s)" % (tb, length, "elements" if length > 1 else "element")

        return r


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


def _change_bus_type(net, bus, bus_type):
    idx = net.bus.index[net.bus["name"] == bus].tolist()[0]
    old_type = net.bus.at[idx, "type"]
    try:
        assert old_type == "NODE"
    except AssertionError:
        msg = "The buses {} is already a {} !".format(bus, old_type)
        logging.error(msg)
        raise ValueError(msg)

    net.bus.at[idx, "type"] = bus_type


def create_empty_network():
    """
    Create an empty network

    :return: a Network object that will later contain all the buses, pipes, etc.
    """
    return _Network()


def create_bus(net, level, name, zone=None):
    """
    Create a bus on a given network

    :param net: the given network
    :param level: nominal pressure level of the bus
    :param name: name of the bus
    :param zone: zone of the bus (default: None)
    :return: name of the bus
    """
    try:
        assert level in net.LEVELS
    except AssertionError:
        msg = "The pressure level of the bus {} is not in {}".format(name, net.LEVELS)
        logging.error(msg)
        raise ValueError(msg)

    idx = len(net.bus.index)
    net.bus.loc[idx] = [name, level, zone, "NODE"]
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


def create_load(net, bus, p_kW, name, min_p_Pa=0.022E5, scaling=1.0):
    """
    Create a load attached to an existing bus in a given network

    :param net: the given network
    :param bus: the existing bus
    :param p_kW: power consumed by the load (in [kW])
    :param name: name of the load
    :param min_p_Pa: minimum acceptable pressure
    :param scaling: scaling factor for the load (default: 1.0)
    :return: name of the load
    """
    _try_existing_bus(net, bus)

    idx = len(net.load.index)
    net.load.loc[idx] = [name, bus, p_kW, min_p_Pa, scaling]

    _change_bus_type(net, bus, "SINK")
    return name


def create_feeder(net, bus, p_lim_kW, p_Pa, name):
    """
    Create a feeder attached to an existing bus in a given network

    :param net: the given network
    :param bus: the existing bus
    :param p_lim_kW: maximum power flowing through the feeder
    :param p_Pa: operating pressure level at the output of the feeder
    :param name: name of the feeder
    :return: name of the feeder
    """
    _try_existing_bus(net, bus)

    idx = len(net.feeder.index)
    net.feeder.loc[idx] = [name, bus, p_lim_kW, p_Pa]

    _change_bus_type(net, bus, "SRCE")
    return name


def create_station(net, bus_high, bus_low, p_lim_kW, p_Pa, name):
    """
    Create a pressure station between two existing buses on different pressure level in a given network

    :param net: the given network
    :param bus_high: the existing bus with higher nominal pressure
    :param bus_low: the existing bus with lower nominal pressure
    :param p_lim_kW: maximum power flowing through the feeder
    :param p_Pa: operating pressure level at the output of the feeder
    :param name: name of the station
    :return: name of the station
    """
    _try_existing_bus(net, bus_high)
    _try_existing_bus(net, bus_low)
    _check_level(net, bus_high, bus_low, same=False)

    idx = len(net.station.index)
    net.station.loc[idx] = [name, bus_high, bus_low, p_lim_kW, p_Pa]

    _change_bus_type(net, bus_high, "SINK")
    _change_bus_type(net, bus_low, "SRCE")
    return name
