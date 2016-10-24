
import numpy as np
from patsy import dmatrix


def aliases(design, model):

    model_matrix = np.array(dmatrix(model, design))
    unaliased_matrix = remove_aliased_columns(model_matrix)
    [alias_coefs, _, _, _] = np.linalg.lstsq(unaliased_matrix, model_matrix)
    return alias_coefs


def remove_aliased_columns(matrix):

    [_, singular_values, _] = np.linalg.svd(matrix)
    return matrix[:, np.array(singular_values > np.finfo(float).eps)]
