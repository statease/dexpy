""" Contains several samplers """

import numpy as np

def uniform_simplex_sample(N, q):
    """ Returns an array of points sampled uniformly from a simplex

    :param N: the number of random sample to be generated
    :param q: the dimension of the simplex
    """
    sample = np.random.exponential(1.0, (N, q))
    row_sums = sample.sum(axis=1)
    sample = sample / row_sums[:, np.newaxis]

    return(sample)
