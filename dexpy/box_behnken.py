import dexpy.design as design
import pandas as pd
import os


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

    Box, G.E.P., and Behnken, D.W., "Some New Three Level Designs for the Study
    of Quantitative Variables", Technometrics, 2, pp. 455-475, 1960.

    :param factor_count: The number of factors to build for.
    :type factor_count: int
    :param center_points: The number of center points to include in the design.
    :type center_points: integer
    """

    factor_names = design.get_factor_names(factor_count)
    csv_path = os.path.join(os.path.dirname(__file__), "data", "BB_{:02d}.csv".format(factor_count))
    factor_data = pd.read_csv(csv_path)
    factor_data.columns = factor_names

    return factor_data
