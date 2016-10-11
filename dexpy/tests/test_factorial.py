from unittest import TestCase

from dexpy.factorial import build_factorial

class TestFactorial(TestCase):

    def test_full(self):

        factor_count = 3
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, design.runs)
