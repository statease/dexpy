"""Functions to build factorial designs."""

import itertools
import pandas as pd
import dexpy.design as design

def get_full_factorial(factor_count):
    factor_data = []
    for run in itertools.product([-1, 1], repeat=factor_count):
        factor_data.append(list(run))
    return factor_data

def build_factorial(factor_count, run_count):
    """Builds a factorial design based on a number of factors and runs.

    If the number of runs requested is a 2**factor_count, this will be a full
    factorial.

    :param factor_count: The number of factors to build for.
    :type factor_count: int
    :param run_count: The number of runs in the resulting design. Must be a power of 2.
    :type run_count: int
    :returns: A pandas.DataFrame object containing the requested design.
    """

    # store minimum aberration generators for factors from 3 to max_factors
    # these are from Design-Expert
    generator_list = {
        3 : { 4 : [ "C=AB" ] },
        4 : { 8 : [ "D=ABC" ] },
        5 : { 8 : [ "D=AB", "E=AC" ], 16 : [ "E=ABCD" ] },
        6 : { 8 : [ "D=AB", "E=AC", "F=BC" ], 16 : [ "E=ABC", "F=BCD" ], 32 : [ "F=ABCD" ] },
        7 : { 8 : [ "D=AB", "E=AC", "F=BC", "G=ABC" ], 16 : [ "E=ABC", "F=BCD", "G=ACD" ], 32 : [ "F=ABCD", "G=ABCE" ], 64 : [ "G=ABCDEF" ] },
    }

    if run_count == 2 ** factor_count:
        return get_full_factorial(factor_count)

    generators = generator_list[factor_count][run_count]
    fractional_factors = len(generators)

    full_factor_count = factor_count - fractional_factors
    full_factor_names = design.get_factor_names(full_factor_count)
    factor_data = pd.DataFrame(get_full_factorial(full_factor_count), columns=full_factor_names)

    for gen in generators:
        lhs, rhs = gen.split("=")
        cols = []
        for var in rhs:
            cols.append(design.get_var_id(var))

        generator_column = factor_data[cols].product(axis=1).rename(lhs)
        factor_data = factor_data.join(generator_column)

    return factor_data
