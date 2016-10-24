from unittest import TestCase

import dexpy.design as design


class TestDesign(TestCase):

    def test_var_name(self):
        """Tests that design converts variable ids into chars correctly."""
        self.assertEqual('A', design.get_var_name(0))
        self.assertEqual('Z', design.get_var_name(24))
        self.assertEqual("A'", design.get_var_name(25))
        self.assertEqual("L'", design.get_var_name(35))
        self.assertEqual("Z'", design.get_var_name(49))
        self.assertEqual('A"', design.get_var_name(50))
        self.assertEqual('C"', design.get_var_name(52))
        self.assertEqual('Z"', design.get_var_name(74))
        # not really valid ids, but we wrap around rather than error
        self.assertEqual('Z', design.get_var_name(-1))
        self.assertEqual('A"', design.get_var_name(75))
