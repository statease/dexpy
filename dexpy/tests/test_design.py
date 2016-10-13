from unittest import TestCase

from dexpy.design import Design

class TestDesign(TestCase):

    def test_var_name(self):
        """Tests that Design converts variable ids into chars correctly."""
        self.assertEqual('A', Design.get_var_name(0))
        self.assertEqual('Z', Design.get_var_name(24))
        self.assertEqual("A'", Design.get_var_name(25))
        self.assertEqual("L'", Design.get_var_name(35))
        self.assertEqual("Z'", Design.get_var_name(49))
        self.assertEqual('A"', Design.get_var_name(50))
        self.assertEqual('C"', Design.get_var_name(52))
        self.assertEqual('Z"', Design.get_var_name(74))
        # not really valid ids, but we wrap around rather than error
        self.assertEqual('Z', Design.get_var_name(-1))
        self.assertEqual('A"', Design.get_var_name(75))
