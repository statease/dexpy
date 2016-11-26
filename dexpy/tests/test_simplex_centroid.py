from unittest import TestCase
from dexpy.simplex_centroid import build_simplex_centroid
from dexpy.eval import det_xtxi
from dexpy.model import make_quadratic_model
import numpy as np
import patsy

class TestSimplexCentroid(TestCase):

    @classmethod
    def test_d_optimality(cls):
        answer_d = [ 2.513455e3, 2.197654e6, 5.52777e9,
                     1.85905e13, 3.447727e16, 1.275709e19 ]

        actual_d = []
        for i in range(3, 9):
            design = build_simplex_centroid(i)
            model = "-1 + " + make_quadratic_model(design.columns,
                                                   include_squared=False)
            x_matrix = patsy.dmatrix(model,
                                     design,
                                     return_type="dataframe")
            actual_d.append(det_xtxi(x_matrix, use_log=False))

        np.testing.assert_allclose(answer_d, actual_d, rtol=1e-5)
