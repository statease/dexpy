from unittest import TestCase

import os
import dexpy.design

class TestLoad(TestCase):

    def test_load(self):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.design = dexpy.design.load(os.path.join(data_dir, "two_fac.xml"))
        self.assertEqual(4, self.design.runs)
        self.assertEqual(2, len(self.design.factors))
        self.assertEqual(1, len(self.design.responses))
