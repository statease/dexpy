import dexpy
import logging
from timeit import default_timer as timer

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger()

factor_count = 12
run_count = 2 ** factor_count

start = timer()
factors = [dexpy.Factor(str(i), "", [0, 1]) for i in range(factor_count)]
design = dexpy.build_factorial(factors, run_count)
end = timer()

logger.debug("time to build {} factor {} run factorial: {}s".format(factor_count, run_count, end - start))

start = timer()
max_order = factor_count - 1
model = dexpy.LinearModel.build_factorial_model(factor_count, max_order)
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
