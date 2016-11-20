from unittest import TestCase
from dexpy.eval import det_xtxi
from dexpy.model import make_quadratic_model
from dexpy.box_behnken import build_box_behnken
import patsy
import numpy as np

class TestBoxBehnken(TestCase):

    def test_three_factor(self):
        """Tests a 3 factor Box-Behnken design."""
        factor_count = 3
        design = build_box_behnken(factor_count)
        self.assertEqual(17, len(design))
        x_matrix = patsy.dmatrix(make_quadratic_model(design.columns),
                                 design,
                                 return_type="dataframe")

        answer_d = -17.551823065312842
        np.testing.assert_allclose(answer_d, det_xtxi(x_matrix), rtol=1e-5)

    def test_five_factor(self):
        """Tests a 5 factor Box-Behnken design."""
        factor_count = 5
        design = build_box_behnken(factor_count)
        self.assertEqual(45, len(design))
        x_matrix = patsy.dmatrix(make_quadratic_model(design.columns),
                                 design,
                                 return_type="dataframe")

        answer_d = -42.74068763678364
        np.testing.assert_allclose(answer_d, det_xtxi(x_matrix), rtol=1e-5)

    def test_six_factor(self):
        """Tests a 6 factor Box-Behnken design."""
        factor_count = 6
        design = build_box_behnken(factor_count)
        self.assertEqual(53, len(design))
        x_matrix = patsy.dmatrix(make_quadratic_model(design.columns),
                                 design,
                                 return_type="dataframe")

        answer_d = -70.8199239661506
        np.testing.assert_allclose(answer_d, det_xtxi(x_matrix), rtol=1e-5)

    def test_twelve_factor(self):
        """Tests a 12 factor Box-Behnken design."""
        factor_count = 12
        design = build_box_behnken(factor_count)
        self.assertEqual(197, len(design))
        x_matrix = patsy.dmatrix(make_quadratic_model(design.columns),
                                 design,
                                 return_type="dataframe")

        answer_d = -285.7997819420118
        np.testing.assert_allclose(answer_d, det_xtxi(x_matrix), rtol=1e-5)

    def test_twentyone_factor(self):
        """Tests a 21 factor Box-Behnken design."""
        factor_count = 21
        design = build_box_behnken(factor_count)
        self.assertEqual(341, len(design))

        x_matrix = patsy.dmatrix(make_quadratic_model(design.columns),
                                 design,
                                 return_type="dataframe")

        answer_d = -765.04475512524230
        np.testing.assert_allclose(answer_d, det_xtxi(x_matrix), rtol=1e-5)
