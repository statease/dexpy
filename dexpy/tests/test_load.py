from unittest import TestCase

import os
import dexpy.design as dsn

class TestLoad(TestCase):

    def test_load(self):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        design = dsn.load_file(os.path.join(data_dir, "two_fac.xml"))
        self.assertEqual(4, dsn.runs(design))

        self.assertEqual(4, len(design['X1']))
        self.assertEqual('1', design['X1'][0])
        self.assertEqual('-1', design['X2'][1])

        self.assertEqual(4, len(design['R1']))
        self.assertEqual(None, design['R1'][0])
        self.assertEqual('2', design['R1'][1])
