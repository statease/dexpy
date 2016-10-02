from unittest import TestCase

import dexpy

class TestFactorial(TestCase):

    def test_full(self):

        factor_count = 3
        run_count = 8
        design = dexpy.build_factorial(factor_count, run_count)
        self.assertEqual(8, design.runs)
