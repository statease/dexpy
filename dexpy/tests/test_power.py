from unittest import TestCase

import os
import math
import dexpy.power
import numpy as np

class TestPower(TestCase):
    """Tests for calculating power."""

    def test_quadratic_power(self):
        """Test power for a quadratic model in a rotatable ccd"""

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

        design = dexpy.design.Design(factor_data, response_data)
        model = dexpy.model.LinearModel.from_string("1 + A + B + AB + A^2 + B^2")
        X = design.create_model_matrix(model)

        power = dexpy.power.power(model, X, 2, 0.05)

        np.testing.assert_almost_equal([1, 49, 49, 28.9, 63.1, 63.1], power)
