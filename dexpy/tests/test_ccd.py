from unittest import TestCase

from dexpy.ccd import build_ccd
import numpy as np

class TestCentralComposite(TestCase):

    def test_fcd(self):
        """Tests a simple 3 factor face-centered central composite design."""

        answer_data = [
            [-1, -1],
            [1, -1],
            [-1, 1],
            [1, 1],
            [-1, 0],
            [1, 0],
            [0, -1],
            [0, 1]
        ]

        ccd_data = build_ccd(2, 1.0)

        np.testing.assert_allclose(ccd_data, answer_data, rtol=1e-4)