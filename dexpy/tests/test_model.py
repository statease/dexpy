from unittest import TestCase

import os
import dexpy.model

class TestTerm(TestCase):

    def test_parse_linear_term(self):

        term = dexpy.model.Term.from_string("A")
        self.assertEqual(1, term.powers[0])

    def test_parse_squared_term(self):

        term = dexpy.model.Term.from_string("A^2D")
        self.assertEqual(2, term.powers[0])
        self.assertEqual(1, term.powers[3])

    def test_parse_coefficient(self):

        term = dexpy.model.Term.from_string("4.1*A")
        self.assertEqual(4.1, term.coefficient)

        term = dexpy.model.Term.from_string("4.1b")
        self.assertEqual(4.1, term.coefficient)

    def test_parse_scientific_coefficient(self):

        term = dexpy.model.Term.from_string('1.2E3*A*C')
        self.assertEqual(1.2e3, term.coefficient)
        self.assertEqual(1, term.powers[0])
        self.assertEqual(1, term.powers[2])

        term = dexpy.model.Term.from_string('1.2e-3*A^3*C')
        self.assertEqual(1.2e-3, term.coefficient)
        self.assertEqual(3, term.powers[0])
        self.assertEqual(1, term.powers[2])

    def test_parse_prime_term(self):

        term = dexpy.model.Term.from_string("A'")
        self.assertEqual(1, term.powers[25])

    def test_parse_double_prime_term(self):

        term = dexpy.model.Term.from_string('P"^2')
        self.assertEqual(2, term.powers[64])

    def test_parse_intercept(self):

        term = dexpy.model.Term.from_string('1')
        self.assertEqual(1, term.coefficient)
        self.assertEqual(0, len(term.powers))

    def test_always_positive(self):

        self.assertTrue(dexpy.model.Term.from_string('A^2').always_positive())
        self.assertFalse(dexpy.model.Term.from_string('A^3').always_positive())
        self.assertTrue(dexpy.model.Term.from_string('A^4').always_positive())
        self.assertTrue(dexpy.model.Term.from_string('A^4B^2').always_positive())
        self.assertFalse(dexpy.model.Term.from_string('A^4C').always_positive())

class TestLinearModel(TestCase):

    def test_parse_model(self):

        model = dexpy.model.LinearModel.from_string("1+A+ 2B +C+AB + 4.1*AbC + 10A*C + A^2 + B^2 + A^2B + AB^2")
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
