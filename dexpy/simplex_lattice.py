"""Functions for building a simplex lattice design."""

import dexpy.design as design
import pandas as pd
import numpy as np
import itertools
from dexpy.model import ModelOrder
from dexpy.eval import count_n_choose_k as count_nk

def build_simplex_lattice(factor_count, model_order = ModelOrder.quadratic):
    """Builds a Simplex Lattice mixture design.

    This design can be used for 2 to 30 components. A simplex-lattice mixture
    design of degree m consists of m+1 points of equally spaced values between
    0 and 1 for each component. If m = 2 then possible fractions are 0, 1/2, 1.
    For m = 3 the possible values are 0, 1/3, 2/3, 1. The points include the
    pure components and enough points between them to estimate an equation of
    degree m. This design differs from a simplex-centroid design by having
    enough points to estimate a full cubic model.

    :param factor_count: The number of mixture components to build for.
    :type factor_count: int
    :param model_order: The order to build for. ModelOrder.linear will choose
                        vertices only (pure blends). ModelOrder.quadratice will
                        add binary blends, and ModelOrder.cubic will add blends
                        of three components.

    :type model_order: dexpy.model.ModelOrder
    """
    run_count = factor_count # pure blends
    if model_order == ModelOrder.quadratic:
        run_count += count_nk(factor_count, 2) # 1/2 1/2 blends
    elif model_order == ModelOrder.cubic:
        # 2/3 1/3 blends (and vice versa)
        run_count += count_nk(factor_count, 2) * 2
        if factor_count > 2:
            run_count += count_nk(factor_count, 3) # 1/3 1/3 1/3 blends

    factor_names = design.get_factor_names(factor_count)
    factor_data = pd.DataFrame(0, columns=factor_names,
                               index=np.arange(0, run_count))

    row = 0
    # always do pure blends
    for combo in itertools.combinations(factor_names, 1):
        factor_data.loc[row, combo] = 1.0
        row += 1

    if model_order == ModelOrder.quadratic:
        # 1/2 1/2 binary blends
        for combo in itertools.combinations(factor_names, 2):
            factor_data.loc[row, combo] = 0.5
            row += 1
    elif model_order == ModelOrder.cubic:
        # 2/3 1/3 blends
        for combo in itertools.combinations(factor_names, 2):
            factor_data.loc[row, combo] = [2/3, 1/3]
            row += 1
            factor_data.loc[row, combo] = [1/3, 2/3]
            row += 1
        # 1/3 1/3 1/3 triple blend
        if factor_count > 2:
            for combo in itertools.combinations(factor_names, 3):
                factor_data.loc[row, combo] = 1/3
                row += 1

    return factor_data
