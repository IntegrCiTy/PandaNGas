#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implementation of the network simulation methods.

    Usage:

    >>>

"""

import numpy as np
import networkx as nx
import pandangas.topology as top

import math
import fluids
import fluids.vectorized as fvec
from scipy.optimize import fsolve
from thermo.chemical import Chemical

# TODO: Simulation order between different pressure level


def _scaled_loads_as_dict(net):
    return {row[1]: row[2]*row[4] for _, row in net.load.iterrows()}


def _p_min_loads_as_dict(net):
    return {row[1]: row[3] for _, row in net.load.iterrows()}


def _graphs_by_level_as_dict(net):
    levels = net.bus["level"].unique()
    g = top.create_nxgraph(net)
    g_dict = {}
    for l in levels:
        nodes = [n for n, data in g.nodes(data=True) if data["level"] == l]
        g_dict[l] = g.subgraph(nodes)
    return g_dict


def _i_mat(graph):
    return nx.incidence_matrix(graph, oriented=True).todense()


def _dp_from_m_dot_vec(m_dot, L, D, eps, fluid):
    A = math.pi * (D/2)**2
    V = m_dot / A / fluid.rho
    Re = fvec.core.Reynolds(V, D, fluid.rho, fluid.mu)
    fd = fvec.friction_factor(Re, eD=eps/D)
    K = fvec.K_from_f(fd=fd, L=L, D=D)
    return fvec.dP_from_K(K, rho=fluid.rho, V=V)


def _eq_m_dot_sum(m_dot_pipes, m_dot_nodes, i_mat):
    node_eq = np.matmul(i_mat, m_dot_pipes) - m_dot_nodes
    return np.asarray(node_eq)[0]


def runpp(net, level="BP", t_grnd=10+273.15):
    g = _graphs_by_level_as_dict(net)[level]

    gas = Chemical('natural gas', T=t_grnd, P=net.LEVELS[level]*1E5)
    material = fluids.nearest_material_roughness('steel', clean=True)
    eps = fluids.material_roughness(material)


