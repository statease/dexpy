import dexpy.factorial
import dexpy.power
import pandas as pd
import numpy as np
import patsy
import statsmodels.formula.api

column_names = ['amount', 'grind_size', 'brew_time', 'grind_type', 'beans']

# calculate power for a 2^5 full factorial
coffee_design = dexpy.factorial.build_factorial(5, 2**5)
coffee_design.columns = column_names
center_points = [
    [0, 0, 0, -1, -1],
    [0, 0, 0, -1, 1],
    [0, 0, 0, 1, -1],
    [0, 0, 0, 1, 1]
]
cp_df = pd.DataFrame(center_points * 2, columns=coffee_design.columns)
coffee_design = coffee_design.append(cp_df)
coffee_design.index = np.arange(0, len(coffee_design))

sn = 2.0
alpha = 0.05
model = ' + '.join(coffee_design.columns)
factorial_power = dexpy.power.f_power(model, coffee_design, sn, alpha)
factorial_power.pop(0) # remove intercept

# convert to %
factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power]
factorial_power = pd.DataFrame(factorial_power,
                               columns=['Power'],
                               index=coffee_design.columns)
print("\nPower for full factorial:")
print(factorial_power)

# calculate power for a 2^5-1 fractional factorial
coffee_design = dexpy.factorial.build_factorial(5, 2**(5-1))
coffee_design.columns = column_names
center_points = [
    [0, 0, 0, -1, -1],
    [0, 0, 0, -1, 1],
    [0, 0, 0, 1, -1],
    [0, 0, 0, 1, 1]
]

coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
coffee_design.index = np.arange(0, len(coffee_design))

model = ' + '.join(coffee_design.columns)
factorial_power = dexpy.power.f_power(model, coffee_design, sn, alpha)
factorial_power.pop(0) # remove intercept
factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %
factorial_power = pd.DataFrame(factorial_power,
                               columns=['Power'],
                               index=coffee_design.columns)

print("\nPower for fractional factorial:")
print(factorial_power)

twofi_model = "(" + '+'.join(coffee_design.columns) + ")**2"
desc = patsy.ModelDesc.from_formula(twofi_model)
factorial_power = dexpy.power.f_power(twofi_model, coffee_design, sn, alpha)
factorial_power.pop(0) # remove intercept
factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %
factorial_power = pd.DataFrame(factorial_power,
                               columns=['Power'], 
                               index=desc.describe().strip("~ ").split(" + "))

print("\nPower for fractional factorial (2FI model):")
print(factorial_power)

# results of the experiment
coffee_design['taste_rating'] = [
    4.4, 5.8, 6.8, 4.6, 2.6, 5, 6.2, 3.4,
    5.6, 5, 5.8, 6.6, 6.2, 3.4, 5, 6.4,
    6, 6, 6.8, 6, 6, 6.2, 5, 6.4
]

lm = statsmodels.formula.api.ols("taste_rating ~" + twofi_model, data=coffee_design).fit()
print(lm.summary2())

reduced_model = "amount + grind_size + brew_time + beans + grind_size:beans"
lm = statsmodels.formula.api.ols("taste_rating ~" + reduced_model, data=coffee_design).fit()
print(lm.summary2())

