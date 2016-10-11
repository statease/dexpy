from unittest import TestCase

import math
from dexpy.design import Design
import numpy as np

class TestModelMatrix(TestCase):
    """Tests for generating a model matrix"""

    def test_quadratic_model(self):
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

        response_data = []

        design = Design(factor_data, response_data)
        X = design.create_model_matrix("1 + A + B + A:B + I(A**2) + I(B**2)")
        np.testing.assert_almost_equal([1.0, axial_pt, 0.0, -0.0, pow(axial_pt, 2), 0.0], X[5])
