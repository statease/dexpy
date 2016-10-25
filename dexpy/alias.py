
import numpy as np
import scipy as sp
from patsy import dmatrix
import logging


def alias_list(design, model):
    """Returns a human-readable list of dependent model columns."""

    model_matrix = dmatrix(model, design, return_type="dataframe")
    logging.debug("model matrix:\n%s", model_matrix)
    alias_coefs = alias_matrix(model_matrix)
    logging.debug("alias matrix:\n%s", alias_coefs)
    aliases = []
    for r in range(alias_coefs.shape[0]):
        alias_strings = []
        for c in range(alias_coefs.shape[1]):
            if c == r:
                continue
            if alias_coefs[r, c] > np.finfo(float).eps:
                if abs(alias_coefs[r, c] - 1.0) > np.finfo(float).eps:
                    alias_strings.append("{}*{}".format(alias_coefs[r, c], model_matrix.columns[c]))
                else:
                    alias_strings.append(model_matrix.columns[c])
        # FIXME: this is incorrect, because the alias matrix does not include
        #        columns that are aliased, so we need to accomodate missing columns
        if len(alias_strings):
            aliases.append("{} = {}".format(model_matrix.columns[r], " + ".join(alias_strings)))
    return aliases


def alias_matrix(model_matrix):
    """Determines which columns of the model are dependent on other columns.

    This is done by solving AX=B, where X is the full rank model matrix,
    and B is all of the columns of the model matrix. The result is a matrix
    of coefficients which represent to what degree a given column is
    collinear with another column.
    """

    model_matrix = np.array(model_matrix)
    # there is no requirement that the model matrix is full rank
    # so first remove linearly dependent columns using LU decomp
    _, _, upper_matrix = sp.linalg.lu(model_matrix)
    logging.debug("upper:\n%s", upper_matrix)
    unaliased_matrix = model_matrix[:, np.array(abs(np.diagonal(upper_matrix)) > np.finfo(float).eps)]
    logging.debug("unaliased:\n%s", unaliased_matrix)

    alias_coefs, _, _, _ = np.linalg.lstsq(unaliased_matrix, model_matrix)
    return alias_coefs
