"""Plots of model effects that assist in model selection."""

import matplotlib.pyplot as pp
import numpy as np
from scipy.stats import t

def plot_pareto(coefficients, standard_errors, residual_df, alpha = 0.05):
    """Draws a pareto plot to the current pyplot figure."""
    effects = []
    for i, _ in enumerate(coefficients):
        effects.append(coefficients[i] / standard_errors[i])

    pp.title("Pareto Chart")
    pp.xlabel("Rank")
    pp.ylabel("t-Value of |Effect|")

    bonferroni_limit = t.ppf(1 - ((alpha / 2) / 7), residual_df)
    t_limit = t.ppf(1 - (alpha / 2), residual_df)

    pp.axhline(y=t_limit, color='b', label="t-Value limit {:0.4f}".format(t_limit))
    pp.axhline(y=bonferroni_limit, color='r', label="Bonferroni Limit {:0.4f}".format(bonferroni_limit))

    heights = []
    bar_colors = []
    for t_value in effects:
        heights.append(abs(t_value))
        if t_value >= 0:
            bar_colors.append('orange')
        else:
            bar_colors.append('b')

    # sort on |t-value|
    heights, bar_colors = (list(x) for x in zip(*sorted(zip(heights, bar_colors), key=lambda pair: pair[0], reverse=True)))
    # alternatively, could use numpy.argsort to get list of indices
    # indices = np.argsort(heights)[::-1]

    x_rank = np.arange(len(heights))
    width = 0.35
    bars = pp.bar(x_rank + width, heights, width, color=bar_colors)
    pp.gca().set_xticks(x_rank + (width * 1.5))
    pp.gca().set_xticklabels([str(i + 1) for i in x_rank])
    pp.gca().set_ylim([0, pp.gca().get_ylim()[1] * 1.1]) # expand the y max a bit so you can see the bonferroni line
    pp.legend()
    return bars
