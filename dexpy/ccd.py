"""Functions for building Central Composite designs."""

import dexpy.design as design
from dexpy.factorial import build_full_factorial
import pandas as pd
import numpy as np
import math
import numbers


def build_ccd(factor_count, alpha="rotatable", center_points=1):
    """Builds a central composite design.

    The most popular response surface method (RSM) design is the central
    composite design (CCD). A CCD has three groups of design points:

    (a) two-level factorial or fractional factorial design points
    (b) axial points (sometimes called "star" points)
    (c) center points

    CCDs are designed to estimate the coefficients of a quadratic model.

    **Factorial Points**

    The two-level factorial part of the design consists of all possible
    combinations of the +1 and -1 levels of the factors. For the two factor case
    there are four design points:

        (-1, -1) (+1, -1) (-1, +1) (+1, +1)

    **Star or Axial Points**

    The star points have all of the factors set to 0, the midpoint, except one
    factor, which has the value +/- Alpha. For a two-factor problem, the star
    points are:

        (-Alpha, 0) (+Alpha, 0) (0, -Alpha) (0, +Alpha)

    The value for Alpha is calculated in each design for both rotatability and
    orthogonality of blocks. The experimenter can choose between these values or
    enter a different one. The default value is set to the rotatable value.

    Another position for the star points is at the face of the cube portion on
    the design. This is commonly referred to as a face-centered central
    composite design. You can create this by setting the alpha distance to one,
    or setting the alpha parameter to "face centered". This design only requires
    three levels for each factor.

    **Center Points**

    Center points, as implied by the name, are points with all levels set to
    coded level 0 - the midpoint of each factor range: (0, 0)

    Center points are usually repeated 4-6 times to get a good estimate of
    experimental error (pure error).

    To summarize, central composite designs require 5 levels of each factor:
    -Alpha, -1, 0, 1, and +Alpha. One of the commendable attributes of the
    central composite design is that its structure lends itself to sequential
    experimentation. Central composite designs can be carried out in blocks.

    **Categorical Factors**

    You may also add categorical factors to this design. This will cause the
    number of runs generated to be multiplied by the number of combinations of
    the categorical factor levels.

    :param factor_count: The number of factors to build for.
    :type factor_count: integer
    :param alpha_type: The alpha to use for the axial points calculate. This can
                       be either a float, in which case the "star" or "axial"
                       points in the design will be placed at that distance. It
                       can also be a string indicating the type of CCD to build
                       e.g. "rotatable".
    :type alpha_type: integer or float
    :param center_points: The number of center points to include in the design.
    :type center_points: integer
    """
    factor_names = design.get_factor_names(factor_count)
    factorial_runs = pd.DataFrame(build_full_factorial(factor_count),
                                  columns=factor_names)

    axial_count = factor_count * 2
    axial_runs = pd.DataFrame(0.0,
                              index=np.arange(0, axial_count),
                              columns=factor_names)

    alpha = alpha_from_type(factor_count, alpha, center_points)
    axial_run = 0
    for f in range(factor_count):
        axial_runs.loc[axial_run][f] = -alpha
        axial_run += 1
        axial_runs.loc[axial_run][f] = alpha
        axial_run += 1
    factor_data = factorial_runs.append(axial_runs)

    center_runs = pd.DataFrame(0.0,
                               index=np.arange(0, center_points),
                               columns=factor_names)
    factor_data = factor_data.append(center_runs)

    return factor_data


def alpha_from_type(factor_count, alpha_type, center_points=0):
    """Calculates an alpha value based on the type of ccd.

    :param factor_count: The number of factors in the ccd.
    :type factor_count: integer
    :param alpha_type: The type of alpha to calculate, e.g. "rotatable". If this
                       parameter is a float, it will be assumed that the alpha
                       is being explicitly set and will be returned immediately.
    :type alpha_type: integer or float
    :param center_points: The number of center points in the design. This
                          affects the calculation of the "orthogonal" alpha
                          type. If the design is blocked this is the center
                          point count in the factorial block.
    :type center_points: integer
    """
    if isinstance(alpha_type, numbers.Real):
        return float(alpha_type)

    # TODO: these should be parameters
    star_reps = 1
    # if the design is blocked this is the center point count in the axial block
    star_center_points = 0
    star_points = factor_count * 2 * star_reps
    factorial_points = 2**factor_count

    if alpha_type == "rotatable":
        return math.sqrt(math.sqrt(factorial_points / star_reps));
    if alpha_type == "spherical":
        return math.sqrt(factor_count)
    if alpha_type == "orthogonal":
        vroot = math.sqrt(factorial_points + star_points + star_center_points +
                          center_points) - math.sqrt(factorial_points)
        qNumerator = vroot * vroot * factorial_points
        qDenominator = 4.0 * star_reps * star_reps
        # alpha = [(VNf)/(4Rs^2)]^(1/4)
        return math.sqrt(math.sqrt(qNumerator/qDenominator))
    if alpha_type == "practical":
        return math.sqrt(math.sqrt(factor_count))
    if (alpha_type == "face centered"
            or alpha_type == "facecentered"
            or alpha_type == "face"):
        return 1.0

    raise ValueError("Didn't recognize alpha type '{}'!".format(alpha_type))
