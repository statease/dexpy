from unittest import TestCase
from dexpy.simplex_lattice import build_simplex_lattice
from dexpy.eval import det_xtxi
from dexpy.model import make_quadratic_model
import numpy as np
import patsy

class TestSimplexLattice(TestCase):

    def test_d_optimality(self):
        answer_d = [
            2, 3, 4,
            5, 6, 7,
            8, 9, 10,
            11, 12, 13,
            14, 15, 16,
            17, 18, 19,
            20, 21, 22,
            23, 24, 25,
            26, 27, 28,
            29, 30,
        ]

        actual_d = []
        for i in range(2, 31):
            design = build_simplex_lattice(i)
            model = "-1 + " + make_quadratic_model(design.columns,
                                                   include_squared=False)
            x_matrix = patsy.dmatrix(model,
                                     design,
                                     return_type="dataframe")
            actual_d.append(det_xtxi(x_matrix, use_log=False))

        np.testing.assert_allclose(answer_d, actual_d, rtol=1e-5)