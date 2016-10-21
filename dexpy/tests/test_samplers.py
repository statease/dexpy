import unittest
import numpy as np
from dexpy.samplers import *

class TestSimplexSampler(unittest.TestCase):
    """ Tests the uniform simplex sampler """

    def test_simplex_sample(self):
        """ Generates a uniform sample, checks dimensions, and that the rows sum to 1 """
        result = uniform_simplex_sample(5, 4)

        self.assertEqual(result.shape[0], 5)
        self.assertEqual(result.shape[1], 4)

        row_sums = np.sum(result, axis=1)
        answer = np.ones(5)

        np.testing.assert_almost_equal(row_sums, answer)

    @classmethod
    def test_simplex_sample_one_component(cls):
        """ Tests an edge case """
        result = uniform_simplex_sample(1, 1)
        answer = np.ones(1)
        np.testing.assert_approx_equal(result, answer)


class TestHitAndRun(unittest.TestCase):

    def test_hit_and_run(self):

        x0 = np.array([0.2, 0.7])
        A = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
        bounds = np.array([1, 1, 0, 0])

        result = hit_and_run(x0, A, bounds, 5, 2)
        self.assertEqual(result.shape[0], 5)
        self.assertEqual(result.shape[1], 2)
