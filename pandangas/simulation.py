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
    return {row[1]: round(row[2]*row[4]/net.LHV, 6) for _, row in net.load.iterrows()}  # kW to kg/s


def _p_nom_feed_as_dict(net):
    feed = {row[1]: row[3] for _, row in net.feeder.iterrows()}
    stat = {row[2]: row[4] for _, row in net.station.iterrows()}
    feed.update(stat)
    return feed


def _p_min_loads_as_dict(net):
    return {row[1]: row[3] for _, row in net.load.iterrows()}


def _i_mat(graph):
    return nx.incidence_matrix(graph, oriented=True).todense()


def _dp_from_m_dot_vec(m_dot, l, d, e, fluid):
    a = math.pi * (d/2)**2
    v = m_dot / a / fluid.rho
    re = fvec.core.Reynolds(v, d, fluid.rho, fluid.mu)
    fd = fvec.friction_factor(re, eD=e/d)
    k = fvec.K_from_f(fd=fd, L=l, D=d)
    return fvec.dP_from_K(k, rho=fluid.rho, V=v)


def _eq_m_dot_sum(m_dot_pipes, m_dot_nodes, i_mat):
    node_eq = np.matmul(i_mat, m_dot_pipes) - m_dot_nodes
    return np.asarray(node_eq)[0]


def _eq_pressure(p_nodes, m_dot_pipes, i_mat, l, d, e, fluid):
    dps_eq = np.matmul(p_nodes, i_mat) + _dp_from_m_dot_vec(m_dot_pipes, l, d, e, fluid)
    return np.asarray(dps_eq)[0]


def _eq_m_dot_node(m_dot_nodes, gr, loads):
    bus_load = np.array([m_dot_nodes[i] - loads[node]
                         for i, (node, data) in enumerate(gr.nodes(data=True)) if data["type"] == "LOAD"])
    bus_node = np.array([m_dot_nodes[i]
                         for i, (node, data) in enumerate(gr.nodes(data=True)) if data["type"] == "NODE"])
    return np.concatenate((bus_load, bus_node))


def _eq_p_feed(p_nodes, gr, p_nom):
    p_feed = np.array([p_nodes[i] - p_nom[node]
                       for i, (node, data) in enumerate(gr.nodes(data=True)) if data["type"] == "FEED"])
    return p_feed


def _init_variables(gr):
    p_nodes_init = np.array([1E5]*len(gr.nodes))
    m_dot_pipes_init = np.array([0.002]*len(gr.edges))
    m_dot_nodes_init = np.array([0.001]*len(gr.nodes))
    return np.concatenate((p_nodes_init, m_dot_pipes_init, m_dot_nodes_init))


def _eq_model(x, *args):
    mat, gr, lengths, diameters, roughness, fluid, loads, p_nom = args
    p_nodes = x[:len(gr.nodes)]
    m_dot_pipes = x[len(gr.nodes):len(gr.nodes)+len(gr.edges)]
    m_dot_nodes = x[len(gr.nodes)+len(gr.edges):]
    return np.concatenate((
        _eq_m_dot_sum(m_dot_pipes, m_dot_nodes, mat),
        _eq_pressure(p_nodes, m_dot_pipes, mat, lengths, diameters, roughness, fluid),
        _eq_m_dot_node(m_dot_nodes, gr, loads),
        _eq_p_feed(p_nodes, gr, p_nom)))


def _run_sim(net, level="BP", t_grnd=10+273.15):
    g = top.graphs_by_level_as_dict(net)[level]

    gas = Chemical('natural gas', T=t_grnd, P=net.LEVELS[level]*1E5)
    material = fluids.nearest_material_roughness('steel', clean=True)
    eps = fluids.material_roughness(material)

    x0 = _init_variables(g)
    i_mat = _i_mat(g)

    leng = np.array([data["L_m"] for _, _, data in g.edges(data=True)])
    diam = np.array([data["D_m"] for _, _, data in g.edges(data=True)])

    load = _scaled_loads_as_dict(net)
    p_nom = _p_nom_feed_as_dict(net)

    res = fsolve(_eq_model, x0, args=(i_mat, g, leng, diam, eps, gas, load, p_nom))

    p_nodes = res[:len(g.nodes)]
    m_dot_pipes = res[len(g.nodes):len(g.nodes) + len(g.edges)]
    m_dot_nodes = res[len(g.nodes) + len(g.edges):]

    return np.round(p_nodes, 1), np.round(m_dot_pipes, 6), np.round(m_dot_nodes, 6)
