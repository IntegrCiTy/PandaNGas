import pandas as pd


class _Network:
    def __init__(self):
        self.bus = pd.DataFrame(columns=["name", "level", "zone", "in_service"])
        self.pipe = pd.DataFrame(columns=["name", "from_bus", "to_bus", "length_m", "diameter_m"])
        self.load = pd.DataFrame(columns=["name", "bus", "p_kw", "scaling"])
        self.feeder = pd.DataFrame(columns=["name", "bus", "p_lim_kw", "p_bar"])
        self.station = pd.DataFrame(columns=["name", "bus_mp", "bus_bp", "p_lim_kw", "p_bar"])


def create_empty_network():
    return _Network()


def create_bus(net, level, name, zone=None, in_service=True):
    assert level in ["MP", "BP"]
    idx = len(net.bus.index)
    net.bus.loc[idx] = [name, level, zone, in_service]
    return name


def create_pipe(net, from_bus, to_bus, length_m, diameter_m, name):
    assert {from_bus, to_bus}.issubset(set(net.bus.name))
    idx = len(net.pipe.index)
    net.pipe.loc[idx] = [name, from_bus, to_bus, length_m, diameter_m]
    return name


def create_load(net, bus, p_kw, name, scaling=1.0):
    assert bus in net.bus.name.unique()
    idx = len(net.load.index)
    net.load.loc[idx] = [name, bus, p_kw, scaling]
    return name


def create_feeder(net, bus, p_lim_kw, p_bar, name):
    assert bus in net.bus.name.unique()
    idx = len(net.feeder.index)
    net.feeder.loc[idx] = [name, bus, p_lim_kw, p_bar]
    return name


def create_station(net, bus_mp, bus_bp, p_lim_kw, p_bar, name):
    assert {bus_mp, bus_bp}.issubset(set(net.bus.name))
    assert net.bus.loc[net.bus.name == bus_mp, "level"].all() == "MP"
    assert net.bus.loc[net.bus.name == bus_bp, "level"].all() == "BP"
    idx = len(net.station.index)
    net.station.loc[idx] = [name, bus_mp, bus_bp, p_lim_kw, p_bar]
    return name
