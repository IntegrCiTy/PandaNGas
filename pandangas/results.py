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


def _index_of_a_bus_in_res(net, bus):
    """
    Return the index of the bus given its name in res_bus DataFrame of a network.
    Return a new index if the bus doesn't exist yet

    :param net: the given network
    :param bus: the name of the bus
    :return: the index of the bus
    """

    if bus in net.res_bus["name"].unique():
        idx = net.res_bus.index[net.res_bus["name"] == bus].tolist()[0]
    else:
        idx = len(net.res_bus.index)

    return idx


def _index_of_a_pipe_in_res(net, pipe):
    """
    Return the index of the pipe given its name in res_pipe DataFrame of a network.
    Return a new index if the pipe doesn't exist yet

    :param net: the given network
    :param pipe: the name of the pipe
    :return: the index of the pipe
    """

    if pipe in net.res_pipe["name"].unique():
        idx = net.res_pipe.index[net.res_bus["name"] == pipe].tolist()[0]
    else:
        idx = len(net.res_pipe.index)

    return idx


def _v_from_m_dot(net, pipe, m_dot, fluid):
    q = m_dot / fluid.rho
    idx = net.pipe.index[net.pipe["name"] == pipe].tolist()[0]
    a = pi * (net.pipe.at[idx, "diameter_m"])**2 / 4
    return q / a


def runpp(net, level="BP", t_grnd=10+273.15):
    p_nodes, m_dot_pipes, m_dot_nodes, fluid = sim._run_sim(net, level, t_grnd)

    for node, value in p_nodes.items():
        if node in net.bus["name"].unique():
            idx = _index_of_a_bus_in_res(net, node)
            net.res_bus.loc[idx] = [node, value]
    net.keys.update("res_bus")

    for pipe, m_dot in m_dot_pipes.items():
        idx = _index_of_a_pipe_in_res(net, pipe)
        v = _v_from_m_dot(net, pipe, m_dot, fluid)
        net.res_pipe.loc[idx] = [pipe, m_dot, v, m_dot * net.LHV, 100*v/net.V_MAX]
    net.keys.update("res_pipe")
