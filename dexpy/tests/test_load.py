from unittest import TestCase

import os
import dexpy

class TestLoad(TestCase):

    def test_load(self):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.design = dexpy.Design.load(os.path.join(data_dir, "two_fac.xml"))
        self.assertEqual(4, self.design.runs)

        self.assertEqual(4, len(self.design.factor_data['A']))
        self.assertEqual('1', self.design.factor_data['A'][0])
        self.assertEqual('-1', self.design.factor_data['B'][1])

        self.assertEqual(4, len(self.design.response_data['R1']))
        self.assertEqual(None, self.design.response_data['R1'][0])
        self.assertEqual('2', self.design.response_data['R1'][1])
