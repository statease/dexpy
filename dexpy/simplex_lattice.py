import dexpy.design as design
import pandas as pd
import numpy as np
from dexpy.model import ModelOrder

def build_simplex_lattice(factor_count, model_order = ModelOrder.quadratic):
    """Builds a Simplex Lattice mixture design.

    This design can be used for 2 to 30 components. A simplex-lattice mixture
    design of degree m consists of m+1 points of equally spaced values between
    0 and 1 for each component. If m = 2 then possible fractions are 0, 1/2, 1.
    For m = 3 the possible values are 0, 1/3, 2/3, 1. The points include the
    pure components and enough points between them to estimate an equation of
    degree m. This design differs from a simplex-centroid design by having
    enough points to estimate a full cubic model.
    """

    run_count = factor_count
    factor_names = design.get_factor_names(factor_count)
    factor_data = pd.DataFrame(0, columns=factor_names,
                                  index=np.arange(0, run_count))

    return factor_data

