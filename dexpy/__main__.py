import dexpy
import logging
from timeit import default_timer as timer

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger()

factor_count = 12
run_count = 2 ** factor_count

start = timer()
design = dexpy.build_factorial(factor_count, run_count)
end = timer()

logger.debug("time to build {} factor {} run factorial: {}s".format(factor_count, run_count, end - start))

start = timer()
max_order = factor_count - 1
model = "(A+B+C+D+E+F+G+H+J+K+L+M)**11" # will generate a 12fi model
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
