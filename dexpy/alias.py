
import numpy as np
import scipy as sp
from patsy import dmatrix


def aliases(design, model):

    model_matrix = dmatrix(model, design)
    _, upper_matrix = sp.linalg.lu(model_matrix, permute_l=True)
    unaliased_matrix = model_matrix[:, np.array(abs(np.diagonal(upper_matrix)) > np.finfo(float).eps)]

    alias_coefs, _, _, _ = np.linalg.lstsq(unaliased_matrix, model_matrix)
    return alias_coefs
