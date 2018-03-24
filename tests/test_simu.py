import numpy as np
import pandangas.simulation as sim
import pandangas.topology as top

import fluids
from thermo.chemical import Chemical

from tests.test_core import fix_create


def test_scaled_loads(fix_create):
    net = fix_create
    assert sim._scaled_loads_as_dict(net) == {'BUS2': 10.0, 'BUS3': 13.0}


def test_p_min_loads(fix_create):
    net = fix_create
    assert sim._p_min_loads_as_dict(net) == {'BUS2': 0.022, 'BUS3': 0.022}


def test_p_nom_feed(fix_create):
    net = fix_create
    assert sim._p_nom_feed_as_dict(net) == {'BUSF': 0.9}


def test_i_mat(fix_create):
    net = fix_create
    g = top.graphs_by_level_as_dict(net)["BP"]
    i_mat = sim._i_mat(g)
    waited = np.array([[1., 0., 1.], [-1., -1., 0.], [0., 1., -1.]])
    assert type(i_mat) is np.matrixlib.defmatrix.matrix
    assert waited[0] in np.asarray(i_mat)
    assert waited[1] in np.asarray(i_mat)
    assert waited[2] in np.asarray(i_mat)


def test_dp_from_m_dot():
    gas = Chemical('natural gas', T=10+273.15, P=4.5E5)
    material = fluids.nearest_material_roughness('steel', clean=True)
    eps = fluids.material_roughness(material)
    assert round(sim._dp_from_m_dot_vec(0.005, 100, 0.05, eps, gas).tolist(), 1) == 61.8


def test_runpp(fix_create):
    net = fix_create
    sim.runpp(net)