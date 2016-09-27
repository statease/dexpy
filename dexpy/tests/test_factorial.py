from unittest import TestCase

import dexpy

class TestFactorial(TestCase):

    def test_full(self):

        factors = [dexpy.Factor(str(i), "", [0, 1]) for i in range(3)]
        design = dexpy.factorial(factors, 8)
        self.assertEqual(8, design.runs)
