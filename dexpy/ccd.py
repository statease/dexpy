
import dexpy.design as design
from dexpy.factorial import build_full_factorial
import pandas as pd
import numpy as np
import math
import numbers


def build_ccd(factor_count, alpha):

    factor_names = design.get_factor_names(factor_count)
    factorial_runs = pd.DataFrame(build_full_factorial(factor_count),
                                  columns=factor_names)

    axial_count = factor_count * 2
    axial_runs = pd.DataFrame(0,
                              index=np.arange(0, axial_count),
                              columns=factor_names)

    alpha = alpha_from_type(factor_count, alpha)
    axial_run = 0
    for f in range(factor_count):
        axial_runs.loc[axial_run][f] = -alpha
        axial_run += 1
        axial_runs.loc[axial_run][f] = alpha
        axial_run += 1
    factor_data = factorial_runs.append(axial_runs)

    return factor_data


def alpha_from_type(factor_count, type):

    if isinstance(type, numbers.Real):
        return type

    # TODO: these should be parameters
    star_reps = 1
    star_center_points = 0
    star_points = factor_count * 2 * star_reps
    factorial_points = 2**factor_count
    factorial_center_points = 0

    if type == "rotatable":
        return math.sqrt(math.sqrt(factorial_points / star_reps));
    if type == "spherical":
        return math.sqrt(factor_count)
    if type == "orthogonal":
        vroot = math.sqrt(factorial_points + star_points + star_center_points + factorial_center_points) - math.sqrt(factorial_points)
        qNumerator = vroot * vroot * factorial_points
        qDenominator = 4.0 * star_reps * star_reps
        # alpha = [(VNf)/(4Rs^2)]^(1/4)
        return math.sqrt(math.sqrt(qNumerator/qDenominator))
    if type == "practical":
        return math.sqrt(math.sqrt(factor_count))
    if type == "face centered" or type == "facecentered" or type == "face":
        return 1.0

    raise ValueError("Didn't recognize alpha type '{}'!".format(type))