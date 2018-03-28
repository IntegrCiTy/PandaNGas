#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implementation of the simulation results gathering methods.

    Usage:

    >>> import pandangas as pg

    >>>

"""

# TODO: proper usage of node VS bus

from math import pi

import pandangas.simulation as sim
from pandangas.utilities import get_index


def _v_from_m_dot(net, pipe, m_dot, fluid):
    q = m_dot / fluid.rho
    idx = net.pipe.index[net.pipe["name"] == pipe].tolist()[0]
    a = pi * (net.pipe.at[idx, "diameter_m"])**2 / 4
    return q / a


def runpp(net, level="BP", t_grnd=10+273.15):
    p_nodes, m_dot_pipes, m_dot_nodes, fluid = sim._run_sim(net, level, t_grnd)

    for node, value in p_nodes.items():
        if node in net.bus["name"].unique():
            idx = get_index(node, net.bus)
            net.res_bus.loc[idx] = [node, value]

    for pipe, m_dot in m_dot_pipes.items():
        idx = get_index(pipe, net.pipe)
        v = _v_from_m_dot(net, pipe, m_dot, fluid)
        net.res_pipe.loc[idx] = [pipe, m_dot, v, m_dot * net.LHV, 100*v/net.V_MAX]

    for node, m_dot in m_dot_nodes.items():
        if node in net.station["bus_low"].unique():
            idx_stat = get_index(node, net.station, col="bus_low")
            stat = net.station.at[idx_stat, "name"]
            idx = get_index(stat, net.res_station)
            net.res_station.loc[idx] = [stat, -m_dot, -m_dot * net.LHV, -100*m_dot*net.LHV/net.station.at[idx_stat, "p_lim_kW"]]
