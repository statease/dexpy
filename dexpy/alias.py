
from patsy import dmatrix
import numpy as np

def aliases(design, model):

    X = np.array(dmatrix(model, design))
    unaliased_X = remove_aliased_columns(X)
    [alias_coefs, resid, rank, s] = np.linalg.lstsq(unaliased_X, X)
    return alias_coefs

def remove_aliased_columns(matrix):

    [u, s, v] = np.linalg.svd(matrix)
    return matrix[:,np.array(s > np.finfo(float).eps)]

