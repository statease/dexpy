"""A worked example of an optimal build using dexpy."""

import dexpy.optimal
from dexpy.model import make_model, ModelOrder
from dexpy.design import coded_to_actual
from patsy import dmatrix
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

reaction_design = dexpy.optimal.build_optimal(2, order=ModelOrder.quadratic)

column_names = ['time', 'temp']
actual_lows = { 'time': 40, 'temp': 80 }
actual_highs = { 'time': 50, 'temp': 90 }

reaction_design.columns = column_names

print(coded_to_actual(reaction_design, actual_lows, actual_highs))


quad_model = make_model(reaction_design.columns, ModelOrder.quadratic)
X = dmatrix(quad_model, reaction_design)
XtX = np.dot(np.transpose(X), X)
d = np.linalg.det(XtX)

print("|(X'X)| for quadratic 2 factor optimal design: {}".format(d))

fg = sns.lmplot('time', 'temp', data=reaction_design, fit_reg=False)
ax = fg.axes[0, 0]
ax.set_xticks([-1, 0, 1])
ax.set_xticklabels(['40 min', '45 min', '50 min'])
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(['80C', '85C', '90C'])
plt.show()

reaction_design = dexpy.optimal.build_optimal(2, run_count=10, order=ModelOrder.quadratic)
reaction_design.columns = column_names
print(coded_to_actual(reaction_design, actual_lows, actual_highs))

X = dmatrix(quad_model, reaction_design)
XtX = np.dot(np.transpose(X), X)
d = np.linalg.det(XtX)

print("|(X'X)| for quadratic 2 factor optimal design with 10 runs: {}".format(d))

fg = sns.lmplot('time', 'temp', data=reaction_design, fit_reg=False)
ax = fg.axes[0, 0]
ax.set_xticks([-1, 0, 1])
ax.set_xticklabels(['40 min', '45 min', '50 min'])
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(['80C', '85C', '90C'])
plt.show()

print("Attempting to build rank-deficient design...")

reaction_design = dexpy.optimal.build_optimal(2, run_count=4, order=ModelOrder.quadratic)
