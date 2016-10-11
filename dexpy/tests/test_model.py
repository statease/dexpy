from unittest import TestCase

from dexpy.model import Term, LinearModel

class TestTerm(TestCase):

    def test_parse_linear_term(self):

        term = Term.from_string("A")
        self.assertEqual(1, term.powers[0])

    def test_parse_squared_term(self):

        term = Term.from_string("A^2D")
        self.assertEqual(2, term.powers[0])
        self.assertEqual(1, term.powers[3])

    def test_parse_coefficient(self):

        term = Term.from_string("4.1*A")
        self.assertEqual(4.1, term.coefficient)

        term = Term.from_string("4.1b")
        self.assertEqual(4.1, term.coefficient)

    def test_parse_scientific_coefficient(self):

        term = Term.from_string('1.2E3*A*C')
        self.assertEqual(1.2e3, term.coefficient)
        self.assertEqual(1, term.powers[0])
        self.assertEqual(1, term.powers[2])

        term = Term.from_string('1.2e-3*A^3*C')
        self.assertEqual(1.2e-3, term.coefficient)
        self.assertEqual(3, term.powers[0])
        self.assertEqual(1, term.powers[2])

    def test_parse_prime_term(self):

        term = Term.from_string("A'")
        self.assertEqual(1, term.powers[25])

    def test_parse_double_prime_term(self):

        term = Term.from_string('P"^2')
        self.assertEqual(2, term.powers[64])

    def test_parse_intercept(self):

        term = Term.from_string('1')
        self.assertEqual(1, term.coefficient)
        self.assertEqual(0, len(term.powers))

    def test_always_positive(self):

        self.assertTrue(Term.from_string('A^2').always_positive())
        self.assertFalse(Term.from_string('A^3').always_positive())
        self.assertTrue(Term.from_string('A^4').always_positive())
        self.assertTrue(Term.from_string('A^4B^2').always_positive())
        self.assertFalse(Term.from_string('A^4C').always_positive())

    def test_invalid_term(self):

        caught = False
        try:
            term = Term.from_string("abi")
        except RuntimeError:
            caught = True
        self.assertTrue(caught)

class TestLinearModel(TestCase):

    def test_parse_model(self):

        model = LinearModel.from_string("1+A+ 2B +C+AB + 4.1*AbC + 10A*C + A^2 + B^2 + A^2B + AB^2")
        self.assertEqual(11, len(model.terms))

        self.assertEqual(1, model.terms[0].coefficient)
        self.assertEqual(0, len(model.terms[0].powers))

        self.assertEqual(1, model.terms[1].coefficient)
        self.assertEqual(1, model.terms[1].powers[0])

        self.assertEqual(2, model.terms[2].coefficient)
        self.assertEqual(1, model.terms[2].powers[1])

        self.assertEqual(1, model.terms[3].coefficient)
        self.assertEqual(1, model.terms[3].powers[2])

        self.assertEqual(1, model.terms[4].coefficient)
        self.assertEqual(1, model.terms[4].powers[0])
        self.assertEqual(1, model.terms[4].powers[1])

        self.assertEqual(4.1, model.terms[5].coefficient)
        self.assertEqual(1, model.terms[5].powers[0])
        self.assertEqual(1, model.terms[5].powers[1])
        self.assertEqual(1, model.terms[5].powers[2])

        self.assertEqual(10, model.terms[6].coefficient)
        self.assertEqual(1, model.terms[6].powers[0])
        self.assertEqual(1, model.terms[6].powers[2])

        self.assertEqual(1, model.terms[7].coefficient)
        self.assertEqual(2, model.terms[7].powers[0])

        self.assertEqual(1, model.terms[8].coefficient)
        self.assertEqual(2, model.terms[8].powers[1])

        self.assertEqual(1, model.terms[9].coefficient)
        self.assertEqual(2, model.terms[9].powers[0])
        self.assertEqual(1, model.terms[9].powers[1])

        self.assertEqual(1, model.terms[10].coefficient)
        self.assertEqual(1, model.terms[10].powers[0])
        self.assertEqual(2, model.terms[10].powers[1])

    def test_factorial_model(self):

        model = LinearModel.build_factorial_model(5, 3)
        self.assertEqual(26, len(model.terms))
        # last term should be CDE
        self.assertEqual(1, model.terms[25].coefficient)
        self.assertEqual(1, model.terms[25].powers[2])
        self.assertEqual(1, model.terms[25].powers[3])
        self.assertEqual(1, model.terms[25].powers[4])

    def test_columns(self):

        model = LinearModel.from_string("1+A+B+C+AB+AC+BC+ABC+A^2")
        self.assertEqual(9, model.columns)

    def test_str(self):

        model = LinearModel.from_string("1+A+B+C+AB+AC+BC+ABC+A^2")
        self.assertEqual('1 + A + B + C + AB + AC + BC + ABC + A^2', str(model))
