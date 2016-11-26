from unittest import TestCase
from dexpy.simplex_lattice import build_simplex_lattice
from dexpy.eval import det_xtxi
from dexpy.model import make_model, ModelOrder
import numpy as np
import patsy

class TestSimplexLattice(TestCase):

    @classmethod
    def test_linear(cls):
        """Checks the optimality of linear simplex lattice designs."""
        answer_d = [ 1 ] * 29
        actual_d = []
        order = ModelOrder.linear
        for i in range(2, 31):
            design = build_simplex_lattice(i, order)
            model = "-1 + " + make_model(design.columns, order,
                                         include_powers=False)
            x_matrix = patsy.dmatrix(model,
                                     design,
                                     return_type="dataframe")
            actual_d.append(det_xtxi(x_matrix, use_log=False))

        np.testing.assert_allclose(answer_d, actual_d, rtol=1e-5)

    @classmethod
    def test_quadratic(cls):
        """Checks the optimality of quadratic simplex lattice designs."""
        answer_d = [
            2.772588722239781, 8.317766166719345, 16.63553233343869,
            27.725887222397816, 41.58883083359672, 58.224363167035406,
            77.63248422271388, 99.81319400063214, 124.76649250079016,
            152.49237972318798, 182.99085566782557, 216.26192033470295,
            252.30557372382012, 291.1218158351771, 332.7106466687738,
            377.0720662246103, 424.2060745026866, 474.1126715030026,
            526.7918572255585, 582.2436316703541, 640.4679948373896,
            701.4649467266647, 765.2344873381797, 831.7766166719344,
            901.091334727929, 973.1786415061633, 1048.0385370066374,
            1125.6710212293513, 1206.076094174305,
        ]
        actual_d = []
        order = ModelOrder.quadratic
        for i in range(2, 31):
            design = build_simplex_lattice(i, order)
            model = "-1 + " + make_model(design.columns, order,
                                         include_powers=False)
            x_matrix = patsy.dmatrix(model,
                                     design,
                                     return_type="dataframe")
            actual_d.append(det_xtxi(x_matrix, use_log=True))

        np.testing.assert_allclose(answer_d, actual_d, rtol=1e-5)

    @classmethod
    def test_cubic(cls):
        """Checks the optimality of cubic simplex lattice designs."""
        answer_d = [
            2.2096470973347775, 13.228395211331954, 39.6547285196038,
            88.08632361788068, 165.1201784728033, 277.35271609131553,
            431.37986869540055, 633.7971466915958, 891.1996956551948,
            1210.1823437751189, 1597.3396416379908, 2059.265895808832,
        ]
        actual_d = []
        order = ModelOrder.cubic
        for i in range(2, 14):
            design = build_simplex_lattice(i, order)
            model = "-1 + " + make_model(design.columns, order,
                                         include_powers=False)
            x_matrix = patsy.dmatrix(model,
                                     design,
                                     return_type="dataframe")
            actual_d.append(det_xtxi(x_matrix, use_log=True))

        np.testing.assert_allclose(answer_d, actual_d, rtol=1e-4)