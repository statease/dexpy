import unittest
import numpy as np
from dexpy.samplers import hit_and_run, uniform_simplex_sample

class TestSimplexSampler(unittest.TestCase):
    """Tests the uniform simplex sampler."""

    def test_simplex_sample(self):
        """Generates a uniform sample, checks dimensions, and that the rows sum to 1."""
        result = uniform_simplex_sample(5, 4)

        self.assertEqual(result.shape[0], 5)
        self.assertEqual(result.shape[1], 4)

        row_sums = np.sum(result, axis=1)
        answer = np.ones(5)
        np.testing.assert_almost_equal(row_sums, answer)

    @classmethod
    def test_simplex_sample_one_component(cls):
        """Tests an edge case."""
        result = uniform_simplex_sample(1, 1)
        answer = np.ones(1)
        np.testing.assert_approx_equal(result, answer)


class TestHitAndRunSquare(unittest.TestCase):
    """Tests the hit and run sampler over [0, 1] x [0, 1]."""

    def setUp(self):

        self.x0 = np.array([0.2, 0.7])
        self.A = np.array([[1, 0],
                           [0, 1],
                           [-1, 0],
                           [0, -1]])
        self.bounds = np.array([1, 1, 0, 0])
        np.random.seed(100)


    def test_hit_and_run_1(self):
        """Tests generation of a single point."""
        result = hit_and_run(self.x0, self.A, self.bounds, 1, 1)
        answer = np.array([[0.57548241, 0.62646417]])
        np.testing.assert_almost_equal(result, answer)


    def test_hit_and_run_2(self):
        """Tests generation of a single point with thin = 3."""
        result = hit_and_run(self.x0, self.A, self.bounds, 1, 3)
        answer = np.array([[0.32222719, 0.10867805]])
        np.testing.assert_almost_equal(result, answer)


    def test_hit_and_run_3(self):
        """Tests generation of 3 points."""
        result = hit_and_run(self.x0, self.A, self.bounds, 2, 1)
        answer = np.array([[0.57548241, 0.62646417],
                           [0.77956909, 0.17414724]])
        np.testing.assert_almost_equal(result, answer)


    def test_hit_and_run_4(self):
        """Tests generation of 3 points with thin = 3."""
        result = hit_and_run(self.x0, self.A, self.bounds, 2, 3)
        answer = np.array([[0.32222719, 0.10867805],
                           [0.30750317, 0.05997018]])
        np.testing.assert_almost_equal(result, answer)


class TestHitAndRunConstrained(unittest.TestCase):
    """Tests the hit and run sampler over [0, 1] x [0, 1].

    With the additional constraint that x1 + x2 > 0.9.
    """

    @classmethod
    def test_hit_and_run_constrained(cls):
        """Tests generation of 4 points."""
        x0 = np.array([0.5, 0.5])
        A = np.array([[1, 0],
                      [0, 1],
                      [-1, 0],
                      [0, -1],
                      [-1, -1]])
        bounds = np.array([1, 1, 0, 0, -0.9])

        np.random.seed(200)

        result = hit_and_run(x0, A, bounds, 4, 1)
        answer = np.array([[0.28429647, 0.78408962],
                           [0.26194012, 0.99263893],
                           [0.30624997, 0.89710025],
                           [0.41753565, 0.74949495]])
        np.testing.assert_almost_equal(result, answer)


class TestHitAndRunOneDimension(unittest.TestCase):
    """Tests the hit and run sampler over [0, 1]."""

    @classmethod
    def test_hit_and_run_one_dim(cls):
        """Tests generation of 2 points with thin = 2."""
        x0 = np.array([0.5])
        A = np.array([[1], [-1]])
        bounds = np.array([1, 0])

        np.random.seed(300)

        result = hit_and_run(x0, A, bounds, 2, 2)
        answer = np.array([[0.70922430],
                           [0.59920946]])
        np.testing.assert_almost_equal(result, answer)

