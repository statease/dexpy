import dexpy
import itertools

def build_factorial(factor_count, run_count):

    factor_data = []
    if run_count == 2 ** factor_count:
        for run in itertools.product([-1, 1], repeat=factor_count):
            factor_data.append(list(run))
    return dexpy.Design(factor_data, [])
