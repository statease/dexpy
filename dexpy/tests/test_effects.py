from unittest import TestCase

from dexpy.effects import plot_pareto

class TestLoad(TestCase):

    def test_pareto_bars(self):
        """Tests the bars on the pareto plot for the Filtrate example data."""
        coefs = [
            10.8125, 4.9375, 7.3125, -9.0625, 8.3125, 1.5625, 0.0625, 1.1875,
            -0.1875, -0.5625, 0.9375, 2.0625, -0.8125, -1.3125, 0.6875
        ]
        se = [ 1.10432 ] * len(coefs)
        residual_df = 10
        bars = plot_pareto(coefs, se, residual_df)

        t_values = [
            9.79106, 8.20638, 7.52723, 6.6217, 4.47106, 1.86766, 1.41489,
            1.18851, 1.07532, 0.848936, 0.735744, 0.622553, 0.509361,
            0.169787, 0.0565957
        ]
        for i, bar in enumerate(bars):
            self.assertAlmostEqual(t_values[i], bar.get_height(), delta=1e-4)
