
def plot_pareto(coefficients, standard_errors):

    effects = []
    for i in range(len(coefficients)):
        effects.append(coefficients[i] / standard_errors[i])
    return effects
