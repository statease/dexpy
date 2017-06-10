from unittest import TestCase
from patsy import dmatrix
import numpy as np
from dexpy.optimal import build_optimal
from dexpy.model import make_model, ModelOrder

class TestOptimal(TestCase):

    def test_optimal(self):
        """Tests a simple 2 factor optimal design

        This is a 6 run design using a quadratic model, from the Meyer and
        Nachtsheim 1995 paper.
        """
        optimal_data = build_optimal(2, order=ModelOrder.quadratic)

        model = make_model(optimal_data.columns, ModelOrder.quadratic, True)
        X = dmatrix(model, optimal_data)
        XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
        d = np.linalg.det(XtXi)

        self.assertAlmostEqual(d, 3.73506e-3, delta=1e-3)

    def test_four_fac_linear(self):
        """Tests a 4 factor optimal design with a linear model.

        This should select 5 corners of the hypercube.
        """
        optimal_data = build_optimal(4, order=ModelOrder.linear)

        model = make_model(optimal_data.columns, ModelOrder.linear, True)
        X = dmatrix(model, optimal_data)
        XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
        d = np.linalg.det(XtXi)

        self.assertAlmostEqual(d, 4.34028E-4, delta=1e-3)

    def test_inverse_build(self):
        """Tests a 4 factor optimal design with an inverse term in the model."""
        model = "X1 + I(1/X2) + X3 + X4"
        optimal_data = build_optimal(4, model=model)

        X = dmatrix(model, optimal_data)
        XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
        d = np.linalg.det(XtXi)

        self.assertAlmostEqual(d, 3.04338E-6, delta=1e-4)

    def test_additional_model_points(self):
        """Tests a 3 factor optimal design with extra points."""
        optimal_data = build_optimal(3,
                                     order=ModelOrder.quadratic,
                                     run_count=20)

        model = make_model(optimal_data.columns, ModelOrder.quadratic, True)
        X = dmatrix(model, optimal_data)
        XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
        d = np.linalg.det(XtXi)

        self.assertAlmostEqual(d, 2.15652E-10, delta=1e-10)

    def test_too_few_points(self):
        """Tests a 3 factor optimal design with insufficient runs."""
        caught_error = False
        try:
            build_optimal(3, order=ModelOrder.quadratic, run_count=5)
        except ValueError:
            caught_error = True

        self.assertTrue(caught_error)

