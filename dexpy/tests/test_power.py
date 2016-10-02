from unittest import TestCase

import os
import math
import dexpy
import numpy as np
import itertools

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

        design = dexpy.Design(factor_data, response_data)
        model = "1 + A + B + A:B + I(A**2) + I(B**2)"
        X = design.create_model_matrix(model)
        power = dexpy.f_power(model, X, 2, 0.05)

        np.testing.assert_allclose(power, [0.2887584, 0.49002743118623, 0.49002743118623, 0.28875325867897, 0.63145653747073, 0.63145653747073], rtol=1e-4)

    def test_large_power(self):

        factor_count = 9

        factor_data = []
        # generate a 2^5 factorial
        for run in itertools.product([-1, 1], repeat=factor_count):
            factor_data.append(list(run))

        response_data = []

        design = dexpy.Design(factor_data, response_data)
        model = "(A+B+C+D+E+F+G+H+J)**4" # will generate a 4fi model
        X = design.create_model_matrix(model)

        power = dexpy.f_power(model, X, 2, 0.05)
