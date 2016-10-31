from unittest import TestCase

from dexpy.ccd import build_ccd
from dexpy.ccd import alpha_from_type
import numpy as np
import patsy

def det_xtxi(x_matrix):
    """Calculates the determinant of the inverse of the information matrix.

    Also known as the D-optimal criterion.

    TODO: move this out of the tests and into a dexpy module
    TODO: should be calculating the log
    """
    xtxi = np.linalg.inv(np.dot(x_matrix.T, x_matrix))
    return np.linalg.det(xtxi)

def make_quadratic_model(factor_names):
    """Creates patsy formula representing a quadratic model for the input terms.

    TODO: move out of tests and into a dexpy module
    """

    interaction_model = "({})**2".format("+".join(factor_names))
    squared_terms = "pow({}, 2)".format(",2)+pow(".join(factor_names))
    return "{}+{}".format(interaction_model, squared_terms)


class TestCentralComposite(TestCase):

    def test_fcd(self):
        """Tests a simple 2 factor face-centered central composite design."""

        ccd_data = build_ccd(2, 1.0)
        x_matrix = patsy.dmatrix(make_quadratic_model(ccd_data.columns),
                                 ccd_data,
                                 return_type="dataframe")

        answer_d = 4.340e-4
        self.assertAlmostEqual(answer_d, det_xtxi(x_matrix))


class TestAlphaParsing(TestCase):

    def test_custom(self):
        """Tests setting a custom alpha value."""
        self.assertAlmostEqual(1.31415, alpha_from_type(5, 1.31415))

    def test_rotatable(self):
        """Tests setting a rotatable alpha value."""
        self.assertAlmostEqual(1.4142135623731, alpha_from_type(2, "rotatable"))
        self.assertAlmostEqual(2.3784142300054, alpha_from_type(5, "rotatable"))
        self.assertAlmostEqual(4.7568284600109, alpha_from_type(9, "rotatable"))

    def test_spherical(self):
        """Tests setting a spherical alpha value."""
        self.assertAlmostEqual(1.4142135623731, alpha_from_type(2, "spherical"))
        self.assertAlmostEqual(2.2360679774998, alpha_from_type(5, "spherical"))
        self.assertAlmostEqual(3.0, alpha_from_type(9, "spherical"))

    def test_orthogonal(self):
        """Tests setting an orthogonal alpha value."""
        self.assertAlmostEqual(0.91017972112445, alpha_from_type(2, "orthogonal"))
        self.assertAlmostEqual(1.5265329278543, alpha_from_type(5, "orthogonal"))
        self.assertAlmostEqual(2.1121386170409, alpha_from_type(9, "orthogonal"))

    def test_practical(self):
        """Tests setting a practical alpha value."""
        self.assertAlmostEqual(1.1892071150027, alpha_from_type(2, "practical"))
        self.assertAlmostEqual(1.4953487812212, alpha_from_type(5, "practical"))
        self.assertAlmostEqual(1.7320508075689, alpha_from_type(9, "practical"))

    def test_face_centered(self):
        """Tests setting a face-centered alpha value."""
        self.assertAlmostEqual(1.0, alpha_from_type(2, "face centered"))
        self.assertAlmostEqual(1.0, alpha_from_type(5, "face centered"))
        self.assertAlmostEqual(1.0, alpha_from_type(9, "face centered"))

    def test_invalid(self):
        caught_exception = False
        try:
            alpha_from_type(45, "beeeeep")
        except ValueError:
            caught_exception = True
        self.assertTrue(caught_exception)

