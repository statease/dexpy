"""Contains several samplers."""

import numpy as np

def uniform_simplex_sample(N, q):
    """Returns an array of points sampled uniformly from a simplex

    :param N: the number of random sample to be generated
    :param q: the dimension of the simplex
    """
    sample = np.random.exponential(1.0, (N, q))
    row_sums = sample.sum(axis=1)
    sample = sample / row_sums[:, np.newaxis]

    return(sample)


def hit_and_run(x0, constraint_matrix, bounds, n_samples, thin = 1):
    """A basic implementation of the hit and run sampler

    :param x0: The starting value of sampler.
    :param constraint_matrix: A matrix of constraints in the form Ax <= b.
    :param bounds: A vector of bounds in the form Ax <= b.
    :param n_samples: The numbers of samples to return.
    :param thin: The thinning factor. Retain every 'thin' sample (e.g. if thin = 2, retain every 2nd sample)
    """
    x = np.copy(x0)
    p = len(x)

    out_samples = np.zeros((n_samples, p))

    for i in range(0, n_samples):
        thin_count = 0

        while thin_count < thin:
            thin_count = thin_count + 1

            random_dir = np.random.normal(0.0, 1.0, p)
            random_dir = random_dir / np.linalg.norm(random_dir)

            denom = constraint_matrix.dot(random_dir)
            intersections = (bounds - constraint_matrix.dot(x)) / denom
            t_low  = np.max(intersections[denom < 0])
            t_high  = np.min(intersections[denom > 0])

            u = np.random.uniform(0, 1)
            random_distance = t_low + u * (t_high - t_low)
            x_new = x + random_distance * random_dir

        out_samples[i, ] = x_new
        x = x_new

    return(out_samples)
