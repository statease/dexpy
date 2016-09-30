import dexpy
import itertools

def build_factorial(factors, runs):

    factor_data = []
    if runs == 2 ** len(factors):
        for run in itertools.product([-1, 1], repeat=len(factors)):
            factor_data.append(list(run))
    return dexpy.Design(factor_data, [])
