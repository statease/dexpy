from unittest import TestCase

import os
import math
import dexpy.design
import dexpy.power
import dexpy.model
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

        np.testing.assert_allclose(power, [0.2887584, 0.49002743118623, 0.49002743118623, 0.28875325867897, 0.63145653747073, 0.63145653747073], rtol=1e-4)
