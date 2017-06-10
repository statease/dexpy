import dexpy.cox_effects as cx
import unittest
import numpy as np

class TestCoxPoints3Components(unittest.TestCase):
    """Tests the generation of points along the Cox effect direction.

    These tests are in 3-component simplex space.
    """

    def setUp(self):
        self.X = np.array([[0.3, 0.23, 0.47], [1, 0, 0]])


    def test_generate_cox_points_1(self):
        """Moves the first coordinate of the first row to a few locations that are passed in."""
        locs = [0, 0.3, 0.5, 1]
        result = cx.generate_cox_points(self.X[0, ], 0, len(locs), locs)

        answer = np.array([[0, 0.32857, 0.671429], [0.3, 0.23, 0.47], [0.5, 0.164286, 0.335714], [1, 0, 0]])
        np.testing.assert_array_almost_equal(result, answer)


    def test_generate_cox_points_2(self):
        """Moves the first coordinate of the second row to a few locations.

        This is an edge case, as the starting values is 1.
        """
        locs = [0, 0.3, 1]
        result = cx.generate_cox_points(self.X[1, ], 0, len(locs), locs)

        answer = np.array([[0, 0.5, 0.5], [0.3, 0.35, 0.35], [1, 0, 0]])
        np.testing.assert_array_almost_equal(result, answer)


    def test_generate_cox_points_3(self):
        """Moves the second coordinate of the second row to a few locations along a grid.

        This is an edge case, as the starting value is 0.
        """
        locs = [0, 0.3, 1]
        result = cx.generate_cox_points(self.X[1, ], 1, len(locs), locs)

        answer = np.array([[1, 0, 0], [0.7, 0.3, 0], [0, 1, 0]])
        np.testing.assert_array_almost_equal(result, answer)


    def test_generate_cox_points_4(self):
        """Moves the first coordinate of the first row to 2 equally spaced points."""
        result = cx.generate_cox_points(self.X[0, ], 0, 1)
        answer = np.array([[0, 0.328571, 0.671428], [1, 0, 0]])
        np.testing.assert_array_almost_equal(result, answer)


    def test_generate_cox_points_5(self):
        """Moves the third coordinate of the first row to 4 equally spaced points."""
        result = cx.generate_cox_points(self.X[0, ], 2, 3)
        answer = np.array([[0.566037, 0.433962, 0], [0.377358, 0.289308, 1/3],
                           [0.188679, 0.144654, 2/3], [0, 0, 1]])
        np.testing.assert_array_almost_equal(result, answer)


class TestCoxPoints2Components(unittest.TestCase):
    """Tests the generation of points along the Cox effect direction in 2-component simplex space."""

    def setUp(self):
        self.X = np.array([[1, 0], [0.5, 0.5]])

    def test_generate_cox_points_1(self):
        """Moves the first coordinate of the first row to 3 equally spaced points."""
        result = cx.generate_cox_points(self.X[0, ], 0, 2)
        answer = np.array([[0, 1], [0.5, 0.5], [1, 0]])
        np.testing.assert_array_almost_equal(result, answer)


    def test_generate_cox_points_2(self):
        """Moves the second coordinate of the first row to 2 equally spaced points."""
        result = cx.generate_cox_points(self.X[0, ], 0, 1)
        answer = np.array([[0, 1], [1, 0]])
        np.testing.assert_array_almost_equal(result, answer)
