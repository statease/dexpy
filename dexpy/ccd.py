
import dexpy.design as design
from dexpy.factorial import build_full_factorial
import pandas as pd

def build_ccd(factor_count, alpha):

    factor_data = pd.DataFrame(build_full_factorial(factor_count),
                               columns=design.get_factor_names(factor_count))
    return factor_data
