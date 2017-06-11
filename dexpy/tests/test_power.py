from unittest import TestCase

import math
import dexpy.design as design
import dexpy.power as power
import numpy as np
import itertools
import pandas as pd

class TestPower(TestCase):
    """Tests for calculating power."""

    @classmethod
    def test_quadratic_power(cls):
        """Test power for a quadratic model in a rotatable ccd."""
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
        model = "1 + X1 + X2 + X1:X2 + I(X1**2) + I(X2**2)"
        power_result = power.f_power(model, factor_data, 2, 0.05)

        power_answers = [
            0.2887584, 0.49002743118623, 0.49002743118623, 0.28875325867897, 0.63145653747073, 0.63145653747073
        ]
        np.testing.assert_allclose(power_result, power_answers, rtol=1e-4)

    @classmethod
    def test_large_power(cls):
        """Test power for a 9 factor model."""
        factor_count = 9

        factor_data = []
        # generate a 2^9 factorial
        for run in itertools.product([-1, 1], repeat=factor_count):
            factor_data.append(list(run))
        factor_data = pd.DataFrame(factor_data, columns=design.get_factor_names(factor_count))

        model = "(X1+X2+X3+X4+X5+X6+X7+X8+X9)**4" # will generate a 4fi model

        power_result = power.f_power(model, factor_data, 0.2, 0.05)

        answer = np.ndarray(256)
        answer.fill(0.61574355066172015)
        answer[0] = 0.99459040972676238
        np.testing.assert_allclose(power_result, answer, rtol=1e-4)
