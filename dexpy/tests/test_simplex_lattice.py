from unittest import TestCase
from dexpy.simplex_lattice import build_simplex_lattice
from dexpy.eval import det_xtxi
from dexpy.model import make_model, ModelOrder
import numpy as np
import patsy

class TestSimplexLattice(TestCase):

    def test_linear(self):
        answer_d = [ 1 ] * 29
        actual_d = []
        for i in range(2, 31):
            order = ModelOrder.linear
            design = build_simplex_lattice(i, order)
            model = "-1 + " + make_model(design.columns, order,
                                         include_powers=False)
            x_matrix = patsy.dmatrix(model,
                                     design,
                                     return_type="dataframe")
            actual_d.append(det_xtxi(x_matrix, use_log=False))

        np.testing.assert_allclose(answer_d, actual_d, rtol=1e-5)