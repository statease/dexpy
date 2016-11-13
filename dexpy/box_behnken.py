from dexpy.factorial import build_factorial
import dexpy.design as design
import pandas as pd
import numpy as np
import math
import itertools


def build_box_behnken(factor_count, center_points = 5):
    """Builds a Box-Behnken design.create_model_matrix

    Box-Behnken designs are response surface designs, specially made to require
    only 3 levels, coded as -1, 0, and +1. Box-Behnken designs are available
    for 3 to 21 factors. They are formed by combining two-level factorial
    designs with incomplete block designs. This procedure creates designs with
    desirable statistical properties but, most importantly, with only a
    fraction of the experiments required for a three-level factorial. Because
    there are only three levels, the quadratic model is appropriate.

    **Center Points**

    Center points, as implied by the name, are points with all levels set to
    coded level 0 - the midpoint of each factor range: (0, 0)

    Center points are usually repeated 4-6 times to get a good estimate of
    experimental error (pure error).

    **Categorical Factors**

    You may also add categorical factors to this design. This will cause the
    number of runs generated to be multiplied by the number of combinations of
    the categorical factor levels.

    :param factor_count: The number of factors to build for.
    :type factor_count: int
    :param center_points: The number of center points to include in the design.
    :type center_points: integer
    """

    # the construction involves creating a 2^2 factorial for each pair of
    # factors, with all other factors set to 0
    # so there are (factor_count choose 2) * (2^2) runs
    factorial_runs = 4
    run_count = center_points + factorial_runs * (math.factorial(factor_count) /
                                     math.factorial(2) /
                                     math.factorial(factor_count - 2))

    factor_names = design.get_factor_names(factor_count)
    factor_data = pd.DataFrame(0, columns=factor_names, index=np.arange(0, run_count))

    factorial = build_factorial(2, factorial_runs)
    start = 0
    for combo in itertools.combinations(factor_names, 2):
        end = start + factorial_runs - 1
        factor_data.loc[start:end, combo[0]] = factorial['A'].tolist()
        factor_data.loc[start:end, combo[1]] = factorial['B'].tolist()
        start += factorial_runs

    return factor_data
