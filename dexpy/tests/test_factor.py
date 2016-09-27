from unittest import TestCase

import os
import dexpy

class TestFactor(TestCase):

    def test_categoric(self):

        factor = dexpy.Factor("A", "", ["1", "2", "L3"])
        self.assertEqual("categoric", factor.type)

    def test_discrete_numeric(self):

        factor = dexpy.Factor("A", "", ["1.1", "1.2", "1.3"])
        self.assertEqual("numeric", factor.type)

    def test_continuous(self):

        factor = dexpy.Factor("A", "", ["1", "10"])
        self.assertEqual("numeric", factor.type)
