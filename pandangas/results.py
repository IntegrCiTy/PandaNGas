#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implementation of the simulation results gathering methods.

    Usage:

    >>> import pandangas as pg

    >>>

"""

import pandangas.simulation as sim


def runpp(net, level="BP", t_grnd=10+273.15):
    p_nodes, m_dot_pipes, m_dot_nodes = sim._run_sim(net, level, t_grnd)
