"""Contains information about a designed experiment."""

from xml.dom import minidom

import string
from patsy import dmatrix
import pandas as pd

valid_vars = string.ascii_uppercase.replace("I", "")


def get_var_name(var_id):
    """Converts a variable id into a character representing that factor."""
    out = valid_vars[var_id % len(valid_vars)]
    if var_id >= len(valid_vars) * 2:
        out += '"'
    elif var_id >= len(valid_vars):
        out += "'"
    return out


def get_var_id(var_name):
    """Returns the index of a variable name."""
    #TODO: need to handle var names with ' or "
    return valid_vars.index(var_name)


def load_file(file_path):
    """Loads a Design-Expert xml file into a pandas DataFrame."""
    xmldoc = minidom.parse(file_path)
    runs = xmldoc.getElementsByTagName('run')

    factor_data = []
    response_data = []

    for r_ele in runs:
        factor_settings = []
        for fac_actual in r_ele.getElementsByTagName('facActual'):
            factor_settings.append(fac_actual.firstChild.nodeValue)
        factor_data.append(factor_settings)

        response_values = []
        for res_val in r_ele.getElementsByTagName('resVal'):
            if res_val.firstChild.nodeValue == "Missing":
                response_values.append(None)
            else:
                response_values.append(res_val.firstChild.nodeValue)
        response_data.append(response_values)

    out_design = pd.DataFrame()
    if factor_data:
        out_design = pd.DataFrame(factor_data, columns=get_factor_names(len(factor_data[0])))
    if response_data:
        out_design = out_design.join(pd.DataFrame(response_data, columns=get_response_names(len(response_data[0]))))
    return out_design


def get_factor_names(factor_count):
    """Returns a list of factor variable names up to the count.

    Example:
        >>> get_factor_names(3)
        ["X1", "X2", "X3"]
    """
    # Design-Expert uses A/B/C for variable names, switching to A'/B'/C'
    # and A"/B"/C" after 25 or 50 variables (I is not used)
    # unfortunately the prime and double prime (single/double quote) characters
    # are not really suitable for strings
    # use X1/X2/X3 instead, which is common in academic material (see the NIST
    # pages,for example)
    # return [get_var_name(i) for i in range(factor_count)]

    return ["X" + str(i+1) for i in range(factor_count)]


def get_response_names(response_count):
    """Returns a list of response variable names up to the count.

    Example:
        >>> get_response_names(3)
        ["R1", "R2", "R3"]
    """
    return ['R' + str(i+1) for i in range(response_count)]


def runs(design):
    """Returns the number of runs in a design."""
    return len(design)


def create_model_matrix(factor_data, formula):
    """Expands a patsy formula into a matrix using a pandas.DataFrame.

    :param factor_data: A pandas.DataFrame that contains factor settings.
    :param formula: A patsy formula that will be used to create the design matrix.
    :returns: A patsy.dmatrix representing the model.
    """
    return dmatrix(formula, factor_data)

def coded_to_actual(coded_data, actual_lows, actual_highs):
    """Converts a pandas DataFrame from coded units to actuals.

    :param coded_data: A pandas.Dataframe that contains the runs to convert.
    :param actual_lows: A dictionary mapping factor names to factor lows.
    :param actual_highs: A dictionary mapping factor names to factor highs.
    :returns: A pandas.DataFrame containing factor settings in actual values.
	"""
    actual_data = coded_data.copy()
    for col in actual_data.columns:
        if not (col in actual_highs and col in actual_lows):
            continue
        try:
            # convert continuous variables to their actual value
            actual_data[col] *= 0.5 * (float(actual_highs[col]) - float(actual_lows[col]))
            # don't need to cast to float here, if either are not a float exception will have been thrown
            actual_data[col] += 0.5 * (actual_highs[col] + actual_lows[col])
        except ValueError:
            # assume 2 level categorical
            actual_data[col] = actual_data[col].map({-1: actual_lows[col], 1: actual_highs[col]})
    return actual_data
