from unittest import TestCase

from dexpy.factorial import build_factorial

class TestFactorial(TestCase):

    def test_full(self):
        """Tests a full two-level factorial."""
        factor_count = 3
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))

    def test_res_v(self):
        """Tests a 2^(5-1) fractional factorial."""
        factor_count = 5
        run_count = 16
        design = build_factorial(factor_count, run_count)
        self.assertEqual(16, len(design))

    def test_res_iii(self):
        """Tests a 2^(7-4) fractional factorial."""
        factor_count = 7
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
