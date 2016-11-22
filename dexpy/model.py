from enum import Enum

class ModelOrder(Enum):

    constant = 0
    linear = 1
    quadratic = 2

def make_quadratic_model(factor_names, include_squared = True):
    """Creates patsy formula representing a quadratic model."""

    interaction_model = "({})**2".format("+".join(factor_names))
    if not include_squared:
        return interaction_model
    squared_terms = "pow({}, 2)".format(",2)+pow(".join(factor_names))
    return "{}+{}".format(interaction_model, squared_terms)