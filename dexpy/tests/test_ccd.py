from unittest import TestCase

from dexpy.ccd import build_ccd
import numpy as np
import patsy

class TestCentralComposite(TestCase):

    def test_fcd(self):
        """Tests a simple 3 factor face-centered central composite design."""

        ccd_data = build_ccd(2, 1.0)
        x_matrix = patsy.dmatrix("A+B+A*B+pow(A,2)+pow(B,2)", ccd_data, return_type="dataframe")

        xtxi = np.linalg.inv(np.dot(x_matrix.T, x_matrix))
        det_xtxi = np.linalg.det(xtxi)

        answer_d = 4.340e-4
        self.assertAlmostEqual(answer_d, det_xtxi)
