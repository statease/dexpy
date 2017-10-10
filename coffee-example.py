#import dexpy
import dexpy.factorial
import dexpy.power
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols

coffee_design = dexpy.factorial.build_factorial(5, 2**(5-1))
coffee_design.columns = ['amount', 'grind_size', 'brew_time', 'grind_type', 'beans']
center_points = [
    [0, 0, 0, -1, -1],
    [0, 0, 0, -1, 1],
    [0, 0, 0, 1, -1],
    [0, 0, 0, 1, 1]
]

actual_lows = { 'amount' : 2.5, 'grind_size' : 8, 'brew_time': 3.5,
                'grind_type': 'burr', 'beans': 'light' }
actual_highs = { 'amount' : 4, 'grind_size' : 10, 'brew_time': 4.5,
                 'grind_type': 'blade', 'beans': 'dark' }
actual_design = dexpy.design.coded_to_actual(coffee_design, actual_lows, actual_highs)
print(actual_design)

coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
coffee_design.index = np.arange(0, len(coffee_design))

twofi_model = "(" + '+'.join(coffee_design.columns) + ")**2"
sn = 2.0
alpha = 0.05
factorial_power = dexpy.power.f_power(twofi_model, coffee_design, sn, alpha)
factorial_power.pop(0)
factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %


coffee_design['taste_rating'] = [
    4.4, 2.6, 2.4, 8.6, 1.6, 2.8, 7.2, 3.4,
    6.8, 3.4, 3.8, 9.0, 5.2, 3.6, 8.2, 7.0,
    5.4, 6.8, 3.6, 5.4, 4.8, 6.2, 4.4, 5.8
]

lm = ols("taste_rating ~" + twofi_model, data=coffee_design).fit()
print(lm.summary2())

#reduced_model = [ x in lm.pvalues
pvalues = lm.pvalues[1:]
reduced_model = '+'.join(pvalues.loc[pvalues < 0.05].index)
print(reduced_model)

lm = ols("taste_rating ~" + reduced_model, data=coffee_design).fit()
print(lm.summary2())

reduced_model = "amount + brew_time + beans + amount:beans + " \
                "grind_size:brew_time + grind_size:grind_type + " \
                "brew_time:grind_type"
lm = ols("taste_rating ~" + reduced_model, data=coffee_design).fit()
print(lm.summary2())
