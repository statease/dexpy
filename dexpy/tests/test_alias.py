from unittest import TestCase

from dexpy.alias import alias_list
import dexpy.design as design
import pandas as pd
import numpy as np


class TestAliases(TestCase):

    def test_two_factors(self):
        """Tests the alias list for two identical factors."""
        factor_data = [
            [-1, -1],
            [-1, -1],
            [1,  1],
            [1,  1],
            [0,  0]
        ]

        factor_names = design.get_factor_names(len(factor_data[0]))
        factor_data = pd.DataFrame(factor_data, columns=factor_names)

        aliases, alias_coefs = alias_list("X1+X2", factor_data)
        answer = [[1, 0, 0], [0, 1, 1]]

        np.testing.assert_allclose(alias_coefs,
                                   answer,
                                   rtol=1e-4,
                                   atol=np.finfo(float).eps)

        answer_list = ["X1 = X2"]
        self.assertEqual(answer_list, aliases)

    def test_pb(self):
        """Tests the alias list for an 11 factor Plackett-Burman design."""
        factor_data = [
            [1, -1, -1, -1, 1, -1, 1, 1, -1, 1, 1],
            [1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1],
            [1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1],
            [-1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1],
            [-1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1],
            [1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1],
            [-1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1],
            [-1, 1, 1, -1, 1, 1, 1, -1, -1, -1, 1],
            [1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1],
            [1, 1, -1, -1, -1, 1, -1, 1, 1, -1, 1],
            [-1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

        factor_names = design.get_factor_names(len(factor_data[0]))
        factor_data = pd.DataFrame(factor_data, columns=factor_names)

        _, alias_coefs = alias_list("(X1+X2+X3+X4+X5+X6+X7+X8+X9+X10+X11)**2", factor_data)

        for r in range(alias_coefs.shape[0]):
            for c in range(alias_coefs.shape[1]):
                self.assertTrue(np.allclose(alias_coefs[r, c], 1.0) or
                                np.allclose(alias_coefs[r, c], 0) or
                                np.allclose(abs(alias_coefs[r, c]), 1/3),
                                "Expected 1, 0 or 1/3 for plackett-burman "
                                "alias, was {}".format(alias_coefs[r, c]))
