from unittest import TestCase

import dexpy.factorial
#import dexpy.design

class TestFactorial(TestCase):

    def test_full(self):

        factors = [dexpy.factor.Factor(str(i), "", [0, 1]) for i in range(3)]
        design = dexpy.factorial.factorial(factors, 8)
        self.assertEqual(8, design.runs)
