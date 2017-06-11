"""Functions to evaluate a design matrix."""

import numpy as np
import math

def det_xtxi(x_matrix, use_log = True):
    """Calculates the determinant of the inverse of the information matrix.

    Also known as the D-optimal criterion.
    """
    xtxi = np.linalg.inv(np.dot(x_matrix.T, x_matrix))
    if use_log:
        sign, logdet = np.linalg.slogdet(xtxi)
        return logdet*sign
    return np.linalg.det(xtxi)


# TODO: move this to a more general utility module
def count_n_choose_k(n, k):
    """Returns the number of k combinations from the set n (n choose k)."""
    return (math.factorial(n) /
            math.factorial(k) /
            math.factorial(n - k))
