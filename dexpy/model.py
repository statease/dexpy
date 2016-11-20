

def make_quadratic_model(factor_names):
    """Creates patsy formula representing a quadratic model."""

    interaction_model = "({})**2".format("+".join(factor_names))
    squared_terms = "pow({}, 2)".format(",2)+pow(".join(factor_names))
    return "{}+{}".format(interaction_model, squared_terms)