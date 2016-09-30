from xml.dom import minidom

import string
import numpy as np
from patsy import dmatrix
import pandas as pd

class Design:
    """Represents a design. Contains factor and response data."""

    valid_vars = string.ascii_uppercase.replace("I", "")

    def __init__(self, factor_data, response_data):

        self.factor_data = pd.DataFrame(factor_data, columns=[Design.get_var_name(i) for i in range(len(factor_data[0]))])
        if len(response_data):
            self.response_data = pd.DataFrame(response_data, columns=['R' + str(i+1) for i in range(len(response_data[0]))])

    @staticmethod
    def get_var_name(var_id):
        out = Design.valid_vars[var_id % len(Design.valid_vars)]
        if var_id >= len(Design.valid_vars) * 2:
            out += '"'
        elif var_id >= len(Design.valid_vars):
            out += "'"
        return out

    @classmethod
    def load(cls, file_path):
        "Loads an xml file into a Design object."

        xmldoc = minidom.parse(file_path)
        factors = xmldoc.getElementsByTagName('factor')
        responses = xmldoc.getElementsByTagName('response')
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

        return cls(factor_data, response_data)

    @property
    def runs(self):
        "Returns the number of runs in the design."
        return len(self.factor_data)

    def create_model_matrix(self, formula):
        """Expands a patsy formula to a matrix using the run and factor settings
           in the design."""
        return dmatrix(formula, self.factor_data)
