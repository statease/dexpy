import numpy as np
from scipy.stats import f
from scipy.stats import ncf

def power(model, model_matrix, effect_size, alpha):

    X = np.array(model_matrix)
    print(X.shape)
    residual_df = X.shape[0] - X.shape[1]

    XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
    non_centrality = 1 / np.diag(XtXi)

    # pre-calculate crit value for 1 df, most common case
    crit_value = f.ppf(1 -alpha, 1, residual_df)

    power = []
    for t in range(0, len(model.terms)):
        nc = adjust_non_centrality(non_centrality[t], model.terms[t])
        nc *= effect_size * effect_size / 4.0
        p = (1 - ncf.cdf(crit_value, 1, residual_df, nc))
        power.append(p)

    return power

def adjust_non_centrality(nc, term):
    """Adjusts the non-centrality parameter for terms that aren't -1 to 1"""
    if term.always_positive():
        return nc * 4 # term goes from 0 to 1
    return nc
