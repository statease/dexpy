from xml.dom import minidom
import numpy as np

class Design:
    """Represents a design. Contains factor and response data."""

    def __init__(self, factor_data, response_data):

        self.factor_data = np.array(factor_data)
        self.response_data = np.array(response_data)

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

    def create_model_matrix(self, model):
        """Expands a model to a matrix using the run and factor settings
           in the design."""

        model_matrix = np.ones((model.columns, self.runs))
        main_effects = self.factor_data.transpose()
        for t in range(len(model.terms)):
            for var_id in model.terms[t].powers:
                for p in range(model.terms[t].powers[var_id]):
                    model_matrix[t] = model_matrix[t] * main_effects[var_id]
        return model_matrix
