"""Functions for building a simplex centroid design."""

import dexpy.design as design
import pandas as pd
import numpy as np
import itertools
from dexpy.eval import count_n_choose_k as count_nk

def build_simplex_centroid(factor_count):
    """Builds a Simplex Centroid mixture design.

    This mixture design can be used for 3 to 8 components. A simplex-centroid
    design consists of all points that are equally weighted mixtures of 1 to q
    components. Included are permutations of:

        Pure blends: (1, 0, ...,0)

        Binary blends: (1/2, 1/2, 0, ...,0)

        Tertiary blends: (1/3, 1/3, 1/3, 0, ...,0)

    and so on to the overall centroid: (1/q, 1/q, ..., 1/q).

    This design differs from a simplex-lattice design. It cannot be used to
    estimate the full cubic model, but can be used to estimate a special cubic
    model.

    :param factor_count: The number of mixture components to build for.
    :type factor_count: int
    """
    run_count = 0
    for i in range(1, factor_count+1):
        run_count += count_nk(factor_count, i)

    factor_names = design.get_factor_names(factor_count)
    factor_data = pd.DataFrame(0, columns=factor_names,
                                  index=np.arange(0, run_count))


    row = 0
    for i in range(1, factor_count+1):
        proportion = 1 / i
        for combo in itertools.combinations(factor_names, i):
            factor_data.loc[row, combo] = proportion
            row += 1


    return factor_data
