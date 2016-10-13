"""Functions to build factorial designs."""

import itertools
import pandas as pd
from dexpy.design import Design

def build_factorial(factor_count, run_count):
    """Builds a factorial design based on a number of factors and runs.

    If the number of runs requested is a 2**factor_count, this will be a full
    factorial.

    Args:
        factor_count (int): The number of factors to build for.
        run_count (int): The number of runs in the resulting desing. Must be
                         a power of 2.
    """
    factor_data = []
    if run_count == 2 ** factor_count:
        for run in itertools.product([-1, 1], repeat=factor_count):
            factor_data.append(list(run))
    else:
        for run in itertools.product([-1, 1], repeat=factor_count-1):
            factor_data.append(list(run))
        factor_data = pd.DataFrame(factor_data)
        generator_column = factor_data.product(axis=1).rename("gen")
        factor_data = factor_data.join(generator_column)

    return Design(factor_data, [])
