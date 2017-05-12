import dexpy.design
import pandas as pd
import numpy as np
import math
from patsy import dmatrix, ModelDesc, build_design_matrices
from dexpy.factorial import build_full_factorial
from dexpy.model import make_model, ModelOrder
from dexpy.samplers import hit_and_run

def update(XtXi, new_point, old_point):
    """rank-2 update of the variance-covariance matrix

    Equation (6) from Meyer and Nachtsheim.
    """

    F2 = np.vstack((new_point, old_point))
    F1 = F2.T.copy()
    F1[:,1] *= -1
    FD = np.dot(F2, XtXi)
    I2x2 = np.identity(2) + np.dot(FD, F1)
    Inverse2x2 = np.linalg.inv(I2x2)
    F2x2FD = np.dot(np.dot(F1, Inverse2x2), FD)
    return XtXi - np.dot(XtXi, F2x2FD)


def delta(X, XtXi, row, new_point, prev_d, use_delta):
    """Calculates the multiplicative change in D-optimality from exchanging
    one point for another in a design.

    This is equation (1) in Meyer and Nachtsheim [MeyerNachtsheim1995]_.

    .. [MeyerNachsheim1995] Meyer, R. K. and Nachtsheim, C.J.,
    "The Coordinate-Exchange Algorithm for Constructing Exact Optimal
    Experimental Designs", Technometrics, 37, pp. 60-69, 1995
    """
    if use_delta:

        old_point = X[row]

        added_variance = np.dot(new_point, np.dot(XtXi, new_point.T))
        removed_variance = np.dot(old_point, np.dot(XtXi, old_point.T))
        covariance = np.dot(new_point, np.dot(XtXi, old_point.T))
        return (
            1 + (added_variance - removed_variance) +
           (covariance * covariance - added_variance * removed_variance)
        )

    else:

        X[row] = new_point
        try:
            XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
            (sign, new_d) = np.linalg.slogdet(XtXi)
        except:
            return 0

        # this is done on the log scale so it's
        # the difference of the old D and new D not the proportion
        return prev_d - new_d


def build_optimal(factor_count, model_order = ModelOrder.quadratic, use_delta = True):
    """Builds an optimal design.

    This uses the Coordinate-Exchange algorithm from Meyer and Nachtsheim 1995.

    Meyer, R. K. and Nachtsheim, C.J., "The Coordinate-Exchange Algorithm for
    Constructing Exact Optimal Experimental Designs", Technometrics, 37,
    pp. 60-69, 1995
    """

    factor_names = dexpy.design.get_factor_names(factor_count)
    model = make_model(factor_names, model_order, True)

    # first generate a valid starting design
    (design, X) = bootstrap(factor_names, model)

    steps = 12
    low = -1
    high = 1

    XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
    (sign, d_optimality) = np.linalg.slogdet(XtXi)

    design_improved = True
    min_change = 0
    swaps = 0
    evals = 0
    if use_delta:
        min_change = 1.0 + np.finfo(float).eps
    while design_improved:

        design_improved = False
        for i in range(0, len(design)):

            design_point = design.iloc[i]

            for f in range(0, factor_count):

                original_value = design_point[f]
                best_step = -1
                best_point = []
                best_change = min_change

                for s in range(0, steps):

                    design_point[f] = low + ((high - low) / (steps - 1)) * s
                    new_point = build_design_matrices([X.design_info], design_point)[0]
                    change_in_d = delta(X, XtXi, i, new_point, d_optimality, use_delta)
                    evals += 1

                    if change_in_d - best_change > np.finfo(float).eps:
                        best_point = new_point
                        best_step = s
                        best_change = change_in_d

                if best_step >= 0:

                    # update X with the best point
                    design_point[f] = low + ((high - low) / (steps - 1)) * best_step
                    if use_delta:
                        XtXi = update(XtXi, best_point, X[i])
                    X[i] = best_point

                    if use_delta:
                        d_optimality -= math.log(best_change)
                    else:
                        d_optimality -= best_change

                    design_improved = True
                    swaps += 1

                else:

                    # restore the original design point value
                    design_point[f] = original_value
                    new_point = build_design_matrices([X.design_info], design_point)[0]
                    X[i] = new_point

    return design

def bootstrap(factor_names, model):
    """Create a minimal starting design that is non-singular."""

    md = ModelDesc.from_formula(model)
    model_size = len(md.rhs_termlist)

    factor_count = len(factor_names)
    x0 = np.zeros(factor_count)
    # add high/low bounds to constraint matrix
    constraint_matrix = np.zeros((factor_count * 2, factor_count))
    bounds = np.zeros(factor_count * 2)
    c = 0
    for f in range(factor_count):
        constraint_matrix[c][f] = -1
        bounds[c] = 1
        c += 1
        constraint_matrix[c][f] = 1
        bounds[c] = 1
        c += 1

    start_points = hit_and_run(x0, constraint_matrix, bounds, model_size)

    d = pd.DataFrame(start_points, columns=factor_names)
    X = dmatrix(model, d)

    return (d, X)

