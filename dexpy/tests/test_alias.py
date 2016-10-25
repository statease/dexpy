from unittest import TestCase

from dexpy.alias import alias_matrix, alias_list
import dexpy.design as design
import pandas as pd
import numpy as np
from patsy import dmatrix
import logging


class TestAliases(TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_two_factors(self):

        factor_data = [
            [-1, -1],
            [-1, -1],
            [1,  1],
            [1,  1],
            [0,  0]
        ]

        factor_data = pd.DataFrame(factor_data, columns=design.get_factor_names(len(factor_data[0])))

        model_matrix = dmatrix("A + B", factor_data)
        logging.debug(alias_list(factor_data, "A + B + A*B"))
        alias_coefs = alias_matrix(model_matrix)
        answer = [[1, 0, 0], [0, 1, 1]]

        np.testing.assert_allclose(alias_coefs, answer, rtol=1e-4, atol=np.finfo(float).eps)
