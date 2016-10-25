from unittest import TestCase

from dexpy.alias import alias_list
import dexpy.design as design
import pandas as pd
import numpy as np


class TestAliases(TestCase):

    def test_two_factors(self):

        factor_data = [
            [-1, -1],
            [-1, -1],
            [1,  1],
            [1,  1],
            [0,  0]
        ]

        factor_names = design.get_factor_names(len(factor_data[0]))
        factor_data = pd.DataFrame(factor_data, columns=factor_names)

        aliases, alias_coefs = alias_list("A+B", factor_data)
        answer = [[1, 0, 0], [0, 1, 1]]

        np.testing.assert_allclose(alias_coefs,
                                   answer,
                                   rtol=1e-4,
                                   atol=np.finfo(float).eps)
