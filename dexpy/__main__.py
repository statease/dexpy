import dexpy
import logging
import statsmodels.api as sm
from statsmodels.formula.api import ols
from timeit import default_timer as timer
import pandas as pd

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger()

factor_count = 4
run_count = 2 ** factor_count

start = timer()
design = dexpy.build_factorial(factor_count, run_count)
end = timer()

# the response data are from the Design-Expert Filtrate example
# see: http://www.statease.com/software/dx10-tut.html
filtrate_data = [45, 43, 68, 75, 48, 45, 80, 70, 71, 100, 60, 86, 65, 104, 65, 96]
design.response_data = pd.DataFrame(filtrate_data, columns=['R1'])

logger.debug("time to build {} factor {} run factorial: {}s".format(factor_count, run_count, end - start))

start = timer()
max_order = factor_count - 1
model = "A + C + D + A:C + A:D"
end = timer()

logger.debug("time to generate {}fi model: {}s".format(max_order, end - start))

start = timer()
X = design.create_model_matrix(model)
end = timer()

logger.debug("time to generate X matrix: {}s".format(end - start))

start = timer()
power = dexpy.f_power(model, X, 2, 0.05)
end = timer()

logger.debug("time to calculate power: {}s".format(end - start))

start = timer()
ols_data = design.factor_data
ols_data = ols_data.join(design.response_data)
lm = ols("R1 ~ " + model, data=ols_data).fit()
print(lm.summary())
end = timer()

logger.debug("time to calculate fit: {}s".format(end - start))

start = timer()
table = sm.stats.anova_lm(lm, typ=2)
end = timer()

logger.debug("time to calculate anova: {}s".format(end - start))

print(table)

print(dexpy.plot_pareto(lm.params, lm.bse))
