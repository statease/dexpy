
import numpy as np
import scipy as sp
import scipy.linalg
from patsy import dmatrix
import math
import logging


def alias_list(model, design):
    """Returns a human-readable list of dependent model columns.

    This is done by solving AX=B, where X is the full rank model matrix,
    and B is all of the columns of the model matrix. The result is a matrix
    of coefficients which represent to what degree a given column is
    collinear with another column.
    """

    # use the square root of machine precision for testing for 0
    epsilon = math.sqrt(np.finfo(float).eps)

    logging.debug("model:\n%s", model)
    model_matrix = dmatrix(model, design, return_type="dataframe")
    logging.debug("model matrix (rhs):\n%s", model_matrix)

    # there is no requirement that the model matrix is full rank
    # so first remove linearly dependent columns using LU decomp
    _, _, upper_matrix = sp.linalg.lu(model_matrix)
    logging.debug("upper matrix from LU:\n%s", upper_matrix)

    column_unaliased = abs(np.diagonal(upper_matrix)) > epsilon
    if model_matrix.shape[0] < model_matrix.shape[1]:
        # if n < p, check the remainder of U for unaliased columns
        column_unaliased = np.append(column_unaliased, upper_matrix[-1:,model_matrix.shape[0]:] > 0)

    logging.debug("found %d columns, X has %d rows", sum(column_unaliased), model_matrix.shape[0])
    # remove estimable column indices until p <= n
    extra_cols = sum(column_unaliased) - model_matrix.shape[0]
    c = len(column_unaliased) - 1
    while extra_cols > 0 and c >= 0:
        if column_unaliased[c]:
            column_unaliased[c] = False
            extra_cols -= 1
        c -= 1
    logging.debug("estimating columns:\n%s", column_unaliased)

    unaliased = model_matrix.loc[:, column_unaliased]
    logging.debug("full rank matrix (lhs):\n%s", unaliased)

    alias_coefs, _, _, _ = np.linalg.lstsq(unaliased, model_matrix)
    logging.debug("alias matrix:\n%s", alias_coefs)
    alias_list = []
    for r in range(alias_coefs.shape[0]):
        alias_strings = []
        for c in range(alias_coefs.shape[1]):
            # all columns are "aliased" with themselves, so don't show
            if unaliased.columns[r] == model_matrix.columns[c]:
                continue
            # 0 means there is no correlation
            if abs(alias_coefs[r, c]) < epsilon:
                continue
            if abs(alias_coefs[r, c] - 1.0) > epsilon:
                alias_strings.append("{}*{}".format(alias_coefs[r, c],
                                     model_matrix.columns[c]))
            else:
                alias_strings.append(model_matrix.columns[c])
        if len(alias_strings):
            alias_list.append("{} = {}".format(unaliased.columns[r],
                              " + ".join(alias_strings)))
    return alias_list, alias_coefs
