"""Functions related to the Cox effects direction."""

import numpy as np

def generate_cox_points(point, coordinate, n_points, new_locs = None):
    """Generates points along the Cox effect direction.

    This calculates several equally-spaced points along the Cox direction of a point.

    :param point: The Cox direction will go through this point
    :param coordinate: The Cox direction will go to this vertex
    :param n_points: The number of points along the Cox effect direction that will be returned
    :param new_locs: A set of locations that the coordinate will be moved to
    """
    q = point.shape[0]

    if new_locs is None:
        new_locs = np.linspace(0, 1, n_points+1)

    cox_points = np.zeros((len(new_locs), q))

    for i in range(0, len(new_locs)):
        nl = new_locs[i]
        cox_points[i, coordinate] = nl

        delta = nl - point[coordinate]

        for j in range(0, q):
            if (j == coordinate):
                continue
            else:
                if (point[coordinate] == 1.0): # TODO:  delta
                    cox_points[i, j] = -delta / (q - 1)
                else:
                    x_j = point[j]
                    cox_points[i, j] = (x_j - (delta * x_j) / (1 - point[coordinate]))

    return cox_points
