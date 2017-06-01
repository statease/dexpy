from unittest import TestCase

from patsy import dmatrix
import numpy as np
from dexpy.optimal import build_optimal
from dexpy.model import make_model, ModelOrder
import time
import random

seed = random.randint(1, 1000)

class TestOptimal(TestCase):

    def setUp(self):
        self.start_time = time.time()
        self.iterations = 1
        np.random.seed(seed)

    def tearDown(self):
        t = time.time() - self.start_time
        print("{}: {}".format(self.id(), t))

    def test_optimal(self):
        """Tests a simple 2 factor optimal design

        This is a 6 run design using a quadratic model, from the Meyer and
        Nachtsheim 1995 paper.
        """

        for i in range(0, self.iterations):
            optimal_data = build_optimal(5, ModelOrder.quadratic, True)

            model = make_model(optimal_data.columns, ModelOrder.quadratic, True)
            X = dmatrix(model, optimal_data)
            XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
            d = np.linalg.det(XtXi)

            print(d)
            self.assertAlmostEqual(d, 3.73506e-3, delta=1e-2)

    def test_optimal_two(self):

        for i in range(0, self.iterations):
            optimal_data = build_optimal(5, ModelOrder.quadratic, False)

            model = make_model(optimal_data.columns, ModelOrder.quadratic, True)
            X = dmatrix(model, optimal_data)
            XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
            d = np.linalg.det(XtXi)

            print(d)
            self.assertAlmostEqual(d, 3.73506e-3, delta=1e-2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SomeTest)
    unittest.TextTestRunner(verbosity=0).run(suite)
