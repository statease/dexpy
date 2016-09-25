from unittest import TestCase

import os
import dexpy.factor

class TestTerm(TestCase):

    def test_categoric(self):

        factor = dexpy.factor.Factor("A", "", ["1", "2", "L3"])
        self.assertEqual("categoric", factor.type)

    def test_discrete_numeric(self):

        factor = dexpy.factor.Factor("A", "", ["1.1", "1.2", "1.3"])
        self.assertEqual("numeric", factor.type)

    def test_continuous(self):

        factor = dexpy.factor.Factor("A", "", ["1", "10"])
        self.assertEqual("numeric", factor.type)
