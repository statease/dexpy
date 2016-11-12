from unittest import TestCase

from dexpy.box_behnken import build_box_behnken

class TestBoxBehnken(TestCase):

    def test_three_factor(self):
        """Tests a 3 factor Box-Behnken design."""
        factor_count = 3
        design = build_box_behnken(factor_count)
        self.assertEqual(17, len(design))