
import dexpy.design as design
import pandas as pd
import numpy as np
from patsy import dmatrix, ModelDesc
from dexpy.factorial import build_full_factorial
from dexpy.model import make_model, ModelOrder
from dexpy.samplers import hit_and_run

def build_optimal(factor_count, model_order = ModelOrder.quadratic):
    """Builds an optimal design.

    This uses the Coordinate-Exchange algorithm from Meyer and Nachtsheim 1995.

    Meyer, R. K. and Nachtsheim, C.J., "The Coordinate-Exchange Algorithm for
    Constructing Exact Optimal Experimental Designs", Technometrics, 37,
    pp. 60-69, 1995
    """

    factor_names = design.get_factor_names(factor_count)
    model = make_model(factor_names, model_order, True)

    # first generate a valid starting design
    start_design = bootstrap(factor_names, model)

    return start_design

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

    return d
