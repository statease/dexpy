
import dexpy.design as design
from dexpy.factorial import build_full_factorial
import pandas as pd
import numpy as np

def build_ccd(factor_count, alpha):

    factor_names = design.get_factor_names(factor_count)
    factorial_runs = pd.DataFrame(build_full_factorial(factor_count),
                               columns=factor_names)

    axial_count = factor_count * 2
    axial_runs = pd.DataFrame(0,
                              index=np.arange(0, axial_count),
                              columns=factor_names)
    axial_run = 0
    for f in range(factor_count):
        axial_runs.loc[axial_run][f] = -alpha
        axial_run += 1
        axial_runs.loc[axial_run][f] = alpha
        axial_run += 1
    factor_data = factorial_runs.append(axial_runs)

    return factor_data
