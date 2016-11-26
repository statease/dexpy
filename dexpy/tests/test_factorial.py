from unittest import TestCase

from dexpy.factorial import build_factorial
from dexpy.alias import alias_list

class TestFactorial(TestCase):

    def test_full(self):
        """Tests a full two-level factorial."""
        factor_count = 3
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
        # should be able to estimate the full 3FI model
        aliases, _ = alias_list("(X1+X2+X3)**3", design)
        self.assertEqual(0, len(aliases))

    def test_res_v(self):
        """Tests a 2^(5-1) fractional factorial."""
        factor_count = 5
        run_count = 16
        design = build_factorial(factor_count, run_count)
        self.assertEqual(16, len(design))
        aliases, _ = alias_list("(X1+X2+X3+X4+X5)**2", design)
        # should be no 2FI aliases in a res v design
        self.assertEqual(0, len(aliases))
        aliases, _ = alias_list("(X1+X2+X3+X4+X5)**3", design)
        # every 2FI should be aliased with a 3FI
        answer_aliases = [
            'X1:X2 = X3:X4:X5',
            'X1:X3 = X2:X4:X5',
            'X1:X4 = X2:X3:X5',
            'X1:X5 = X2:X3:X4',
            'X2:X3 = X1:X4:X5',
            'X2:X4 = X1:X3:X5',
            'X2:X5 = X1:X3:X4',
            'X3:X4 = X1:X2:X5',
            'X3:X5 = X1:X2:X4',
            'X4:X5 = X1:X2:X3'
        ]
        self.assertEqual(answer_aliases, aliases)

    def test_res_iii(self):
        """Tests a 2^(6-3) fractional factorial."""
        factor_count = 6
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
        model = "(X1+X2+X3+X4+X5+X6)**2"
        aliases, _ = alias_list(model, design)
        answer_aliases = [
            'X1 = X2:X4 + X3:X5',
            'X2 = X1:X4 + X3:X6',
            'X3 = X1:X5 + X2:X6',
            'X4 = X1:X2 + X5:X6',
            'X5 = X1:X3 + X4:X6',
            'X6 = X2:X3 + X4:X5',
            'X1:X6 = X2:X5 + X3:X4',
        ]
        self.assertEqual(answer_aliases, aliases)

    def test_res_iii_seven_fac(self):
        """Tests a 2^(7-4) fractional factorial."""
        factor_count = 7
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
        aliases, _ = alias_list("(X1+X2+X3+X4+X5+X6+X7)**2", design)
        answer_aliases = [
            'X1 = X2:X4 + X3:X5 + X6:X7', 'X2 = X1:X4 + X3:X6 + X5:X7',
            'X3 = X1:X5 + X2:X6 + X4:X7', 'X4 = X1:X2 + X3:X7 + X5:X6',
            'X5 = X1:X3 + X2:X7 + X4:X6', 'X6 = X1:X7 + X2:X3 + X4:X5',
            'X7 = X1:X6 + X2:X5 + X3:X4'
        ]
        self.assertEqual(answer_aliases, aliases)

    def test_res_iii_21_fac(self):
        """Tests a 2^(21-16) fractional factorial."""
        factor_count = 21
        run_count = 32
        design = build_factorial(factor_count, run_count)
        self.assertEqual(32, len(design))
        model = "(X1+X2+X3+X4+X5+X6+X7+X8+X9+X10+X11+X12+X13+X14+X15+X16+X17+X18+X19+X20+X21)**2"
        aliases, _ = alias_list(model, design)
        answer_aliases = [
            'X1 = X9:X10 + X13:X14 + X16:X17 + X18:X19 + X20:X21',
            'X2 = X8:X10 + X12:X14 + X15:X17 + X18:X20 + X19:X21',
            'X3 = X7:X10 + X11:X14 + X15:X19 + X16:X20 + X17:X21',
            'X4 = X6:X10 + X11:X17 + X12:X19 + X13:X20 + X14:X21',
            'X5 = X6:X14 + X7:X17 + X8:X19 + X9:X20 + X10:X21',
            'X6 = X4:X10 + X5:X14 + X15:X20 + X16:X19 + X17:X18',
            'X7 = X3:X10 + X5:X17 + X12:X20 + X13:X19 + X14:X18',
            'X8 = X2:X10 + X5:X19 + X11:X20 + X13:X17 + X14:X16',
            'X9 = X1:X10 + X5:X20 + X11:X19 + X12:X17 + X14:X15',
            'X10 = X1:X9 + X2:X8 + X3:X7 + X4:X6 + X5:X21 + X11:X18 + X12:X16 + X13:X15',
            'X11 = X3:X14 + X4:X17 + X8:X20 + X9:X19 + X10:X18',
            'X12 = X2:X14 + X4:X19 + X7:X20 + X9:X17 + X10:X16',
            'X13 = X1:X14 + X4:X20 + X7:X19 + X8:X17 + X10:X15',
            'X14 = X1:X13 + X2:X12 + X3:X11 + X4:X21 + X5:X6 + X7:X18 + X8:X16 + X9:X15',
            'X15 = X2:X17 + X3:X19 + X6:X20 + X9:X14 + X10:X13',
            'X16 = X1:X17 + X3:X20 + X6:X19 + X8:X14 + X10:X12',
            'X17 = X1:X16 + X2:X15 + X3:X21 + X4:X11 + X5:X7 + X6:X18 + X8:X13 + X9:X12',
            'X18 = X1:X19 + X2:X20 + X6:X17 + X7:X14 + X10:X11',
            'X19 = X1:X18 + X2:X21 + X3:X15 + X4:X12 + X5:X8 + X6:X16 + X7:X13 + X9:X11',
            'X20 = X1:X21 + X2:X18 + X3:X16 + X4:X13 + X5:X9 + X6:X15 + X7:X12 + X8:X11',
            'X21 = X1:X20 + X2:X19 + X3:X17 + X4:X14 + X5:X10',
            'X1:X2 = X3:X6 + X4:X7 + X5:X11 + X8:X9 + X12:X13 + X15:X16 + X18:X21 + X19:X20',
            'X1:X3 = X2:X6 + X4:X8 + X5:X12 + X7:X9 + X11:X13 + X15:X18 + X16:X21 + X17:X20',
            'X1:X4 = X2:X7 + X3:X8 + X5:X15 + X6:X9 + X11:X16 + X12:X18 + X13:X21 + X14:X20',
            'X1:X5 = X2:X11 + X3:X12 + X4:X15 + X6:X13 + X7:X16 + X8:X18 + X9:X21 + X10:X20',
            'X1:X6 = X2:X3 + X4:X9 + X5:X13 + X7:X8 + X11:X12 + X15:X21 + X16:X18 + X17:X19',
            'X1:X7 = X2:X4 + X3:X9 + X5:X16 + X6:X8 + X11:X15 + X12:X21 + X13:X18 + X14:X19',
            'X1:X8 = X2:X9 + X3:X4 + X5:X18 + X6:X7 + X11:X21 + X12:X15 + X13:X16 + X14:X17',
            'X1:X11 = X2:X5 + X3:X13 + X4:X16 + X6:X12 + X7:X15 + X8:X21 + X9:X18 + X10:X19',
            'X1:X12 = X2:X13 + X3:X5 + X4:X18 + X6:X11 + X7:X21 + X8:X15 + X9:X16 + X10:X17',
            'X1:X15 = X2:X16 + X3:X18 + X4:X5 + X6:X21 + X7:X11 + X8:X12 + X9:X13 + X10:X14'
        ]

        self.assertEqual(answer_aliases, aliases)
