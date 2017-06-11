"""Functions for creating and working with a model."""

from enum import Enum

class ModelOrder(Enum):
    """Represents a full model order."""

    constant = 0
    linear = 1
    quadratic = 2
    cubic = 3

def make_quadratic_model(factor_names, include_squared = True):
    """Creates patsy formula representing a quadratic model."""
    return make_model(factor_names, ModelOrder.quadratic, include_squared)

def make_model(factor_names, model_order, include_powers = True):
    """Creates patsy formula representing a given model order."""
    if model_order == ModelOrder.quadratic:
        interaction_model = "({})**2".format("+".join(factor_names))
        if not include_powers:
            return interaction_model
        squared_terms = "pow({}, 2)".format(",2)+pow(".join(factor_names))
        return "{}+{}".format(interaction_model, squared_terms)

    if model_order == ModelOrder.cubic:
        interaction_model = "({})**3".format("+".join(factor_names))
        if not include_powers:
            return interaction_model
        squared_terms = "pow({}, 2)".format(",2)+pow(".join(factor_names))
        cubed_terms = "pow({}, 3)".format(",3)+pow(".join(factor_names))
        return "+".join([interaction_model, squared_terms, cubed_terms])

    return "+".join(factor_names)
