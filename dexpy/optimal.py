import dexpy.design
import pandas as pd
import numpy as np
from patsy import dmatrix, ModelDesc, build_design_matrices
from dexpy.factorial import build_full_factorial
from dexpy.model import make_model, ModelOrder
from dexpy.samplers import hit_and_run

def delta(X, row, new_point, prev_d):
    """Calculates the multiplicative change in D-optimality from exchanging
    one point for another in a design.

    This is equation (1) in Meyer and Nachtsheim [MeyerNachtsheim1995]_.

    NB: right now this is being done on the log scale so it's
        the difference of the old D and new D not the proportion

    .. [MeyerNachsheim1995] Meyer, R. K. and Nachtsheim, C.J.,
    "The Coordinate-Exchange Algorithm for Constructing Exact Optimal
    Experimental Designs", Technometrics, 37, pp. 60-69, 1995
    """

    X[row] = new_point
    try:
        XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
        (sign, new_d) = np.linalg.slogdet(XtXi)
    except:
        return 0
    return prev_d - new_d


def build_optimal(factor_count, model_order = ModelOrder.quadratic):
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
    while design_improved:

        design_improved = False
        for i in range(0, len(design)):

            design_point = design.iloc[i]

            for f in range(0, factor_count):

                original_value = design_point[f]
                best_step = -1
                best_point = []

                for s in range(0, steps):

                    design_point[f] = low + ((high - low) / (steps - 1)) * s
                    new_point = build_design_matrices([X.design_info], design_point)[0]
                    change_in_d = delta(X, i, new_point, d_optimality)

                    if change_in_d > 0:
                        best_point = new_point
                        best_step = s
                        d_optimality -= change_in_d

                if best_step >= 0:

                    # update X with the best point
                    design_point[f] = low + ((high - low) / (steps - 1)) * best_step
                    X[i] = best_point
                    design_improved = True

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

    x0 = np.array([0, 0])
    # add high/low bounds to constraint matrix
    factor_count = len(factor_names)
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

