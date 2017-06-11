"""Functions for creating an optimal design."""

import dexpy.design
import pandas as pd
import numpy as np
import math
import logging
from patsy import dmatrix, ModelDesc
from dexpy.model import make_model, ModelOrder
from dexpy.samplers import hit_and_run

def update(XtXi, new_point, old_point):
    """rank-2 update of the variance-covariance matrix

    Equation (6) from Meyer and Nachtsheim :cite:`MeyerNachtsheim1995`.
    """
    F2 = np.vstack((new_point, old_point))
    F1 = F2.T.copy()
    F1[:,1] *= -1
    FD = np.dot(F2, XtXi)
    I2x2 = np.identity(2) + np.dot(FD, F1)
    Inverse2x2 = np.linalg.inv(I2x2)
    F2x2FD = np.dot(np.dot(F1, Inverse2x2), FD)
    return XtXi - np.dot(XtXi, F2x2FD)

def expand_point(design_point, code):
    """Converts a point in factor space to conform with the X matrix."""
    return np.array(eval(code, {}, design_point))

def delta(X, XtXi, row, new_point):
    """Calculates the change in D-optimality from exchanging a point.

    This is equation (1) in Meyer and Nachtsheim :cite:`MeyerNachtsheim1995`.
    """
    old_point = X[row]

    added_variance = np.dot(new_point, np.dot(XtXi, new_point.T))
    removed_variance = np.dot(old_point, np.dot(XtXi, old_point.T))
    covariance = np.dot(new_point, np.dot(XtXi, old_point.T))
    return (
        1 + (added_variance - removed_variance) +
            (covariance * covariance - added_variance * removed_variance)
    )

def build_optimal(factor_count, **kwargs):
    r"""Builds an optimal design.

    This uses the Coordinate-Exchange algorithm from Meyer and Nachtsheim 1995
    :cite:`MeyerNachtsheim1995`.

    :param factor_count: The number of factors to build for.
    :type factor_count: integer

    :Keyword Arguments:
        * **order** (:class:`ModelOrder <dexpy.model.ModelOrder>`) -- \
            Builds a design for this order model.\
            Mutually exclusive with the **model** parameter.
        * **model** (`patsy formula <https://patsy.readthedocs.io>`_) -- \
            Builds a design for this model formula. \
            Mutually exclusive with the **order** parameter.
        * **run_count** (`integer`) -- \
            The number of runs to use in the design. This must be equal\
            to or greater than the rank of the model.
    """
    factor_names = dexpy.design.get_factor_names(factor_count)

    model = kwargs.get('model', None)
    if model is None:
        order = kwargs.get('order', ModelOrder.quadratic)
        model = make_model(factor_names, order, True)

    run_count = kwargs.get('run_count', 0)

    # first generate a valid starting design
    (design, X) = bootstrap(factor_names, model, run_count)

    functions = []
    for _, subterms in X.design_info.term_codings.items():
        sub_funcs = []
        for subterm in subterms:
            for factor in subterm.factors:
                eval_code = X.design_info.factor_infos[factor].state['eval_code']
                if eval_code[0] == 'I':
                    eval_code = eval_code[1:]
                sub_funcs.append(eval_code)
        if not sub_funcs:
            functions.append("1") # intercept
        else:
            functions.append("*".join(sub_funcs))

    full_func = "[" + ",".join(functions) + "]"
    code = compile(full_func, "<string>", "eval")

    steps = 12
    low = -1
    high = 1

    XtXi = np.linalg.inv(np.dot(np.transpose(X), X))
    (_, d_optimality) = np.linalg.slogdet(XtXi)

    design_improved = True
    swaps = 0
    evals = 0
    min_change = 1.0 + np.finfo(float).eps
    while design_improved:

        design_improved = False
        for i in range(0, len(design)):

            design_point = design.iloc[i]

            for f in range(0, factor_count):

                original_value = design_point[f]
                original_expanded = X[i]
                best_step = -1
                best_point = []
                best_change = min_change

                for s in range(0, steps):

                    design_point[f] = low + ((high - low) / (steps - 1)) * s
                    new_point = expand_point(design_point, code)
                    change_in_d = delta(X, XtXi, i, new_point)
                    evals += 1

                    if change_in_d - best_change > np.finfo(float).eps:
                        best_point = new_point
                        best_step = s
                        best_change = change_in_d

                if best_step >= 0:

                    # update X with the best point
                    design_point[f] = low + ((high - low) / (steps - 1)) * best_step
                    XtXi = update(XtXi, best_point, X[i])
                    X[i] = best_point

                    d_optimality -= math.log(best_change)
                    design_improved = True
                    swaps += 1

                else:

                    # restore the original design point value
                    design_point[f] = original_value
                    X[i] = original_expanded

    logging.info("{} swaps evaluated, {} executed ({:.2f}%)".format(evals, swaps, 100*(swaps / evals)))

    return design

def bootstrap(factor_names, model, run_count):
    """Create a minimal starting design that is non-singular."""
    md = ModelDesc.from_formula(model)
    model_size = len(md.rhs_termlist)
    if run_count == 0:
        run_count = model_size
    if model_size > run_count:
        raise ValueError("Can't build a design of size {} "
                         "for a model of rank {}. "
                         "Model: '{}'".format(run_count, model_size, model))

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

    start_points = hit_and_run(x0, constraint_matrix, bounds, run_count)

    d = pd.DataFrame(start_points, columns=factor_names)
    X = dmatrix(model, d)

    return (d, X)
