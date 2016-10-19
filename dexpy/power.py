"""Functions to calculate statistical power for a design."""

import numpy as np
from scipy.stats import f
from scipy.stats import ncf

def f_power(model_matrix, effect_size, alpha):
    """Calculates the power of an F test.

    This calculates the probability that the F-statistic is above its critical
    value (alpha) given an effect of some size.

    :param model_matrix: A patsy design matrix
    :type model_matrix: patsy.dmatrix
    :param effect_size: The size of the effect that the test should be able to detect (also called a signal to noise
        ratio).
    :type effect_size: float
    :param alpha: The critical value that we want the test to be above.
    :type alpha: float between 0 and 1
    :returns: A list of percentage probabilities that an F-test could detect an effect of the given size at the given
        alpha value for a particular column.
    """
    X = model_matrix
    residual_df = X.shape[0] - X.shape[1]

    XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
    non_centrality = 1 / np.diag(XtXi)

    # pre-calculate crit value for 1 df, most common case
    crit_value = f.ppf(1 - alpha, 1, residual_df)

    power = []
    for t in range(0, X.shape[1]):
        nc = adjust_non_centrality(non_centrality[t], X[:,t])
        nc *= effect_size * effect_size / 4.0
        p = (1 - ncf.cdf(crit_value, 1, residual_df, nc))
        power.append(p)

    return power

def adjust_non_centrality(nc, x_col):
    """Adjusts the non-centrality parameter for terms that aren't -1 to 1."""
    if always_positive(x_col):
        return nc * 4 # term goes from 0 to 1
    return nc

def always_positive(x_col):
    """Checks that a column is always positive in the design space."""
    return np.all(x_col >= 0)
