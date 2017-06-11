"""Functions for detecting and listing aliases."""

import numpy as np
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

    Usage:
      >>> design = dexpy.factorial.build_factorial(4, 8)
      >>> aliases, alias_coefs = dexpy.alias.alias_list("(A+B+C+D)**2)", design)
      >>> print(aliases)
      ['A:B = C:D', 'A:C = B:D', 'A:D = B:C']
    """
    # use the square root of machine precision for testing for 0
    epsilon = math.sqrt(np.finfo(float).eps)

    logging.debug("model:\n%s", model)
    model_matrix = dmatrix(model, design, return_type="dataframe")
    logging.debug("model matrix (rhs):\n%s", model_matrix)

    # there is no requirement that the model matrix is full rank
    # so first remove linearly dependent columns using LU decomp
    _, _, upper_matrix = scipy.linalg.lu(model_matrix)

    row = 0
    col = 0
    # this array will be used to select columns for the full rank X matrix
    column_unaliased = [False] * model_matrix.shape[1]
    # iterate over diagonals of U, skipping columns with 0 in the diagonal
    while row < model_matrix.shape[0] and col < model_matrix.shape[1]:
        if abs(upper_matrix[row, col]) > epsilon:
            column_unaliased[col] = True
            row += 1
        col += 1
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
        if alias_strings:
            alias_list.append("{} = {}".format(unaliased.columns[r],
                              " + ".join(alias_strings)))
    return alias_list, alias_coefs
