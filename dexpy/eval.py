import numpy as np


def det_xtxi(x_matrix, use_log = True):
    """Calculates the determinant of the inverse of the information matrix.

    Also known as the D-optimal criterion.
    """
    xtxi = np.linalg.inv(np.dot(x_matrix.T, x_matrix))
    if use_log:
        sign, logdet = np.linalg.slogdet(xtxi)
        return logdet*sign
    else:
        return np.linalg.det(xtxi)
