from unittest import TestCase

import math
import dexpy.design as design
import numpy as np
import pandas as pd

class TestModelMatrix(TestCase):
    """Tests for generating a model matrix"""

    @classmethod
    def test_quadratic_model(cls):
        """Test expanding a quadratic model in a rotatable ccd"""
        axial_pt = math.sqrt(2)
        factor_data = [
            [-1, -1],
            [ 1, -1],
            [-1,  1],
            [ 1,  1],
            [-axial_pt, 0],
            [axial_pt, 0],
            [ 0, -axial_pt],
            [ 0, axial_pt],
            [ 0, 0]
        ]

        factor_data = pd.DataFrame(factor_data, columns=design.get_factor_names(len(factor_data[0])))
        X = design.create_model_matrix(factor_data, "1 + X1 + X2 + X1:X2 + I(X1**2) + I(X2**2)")
        np.testing.assert_almost_equal([1.0, axial_pt, 0.0, -0.0, pow(axial_pt, 2), 0.0], X[5])
