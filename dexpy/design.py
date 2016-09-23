from xml.dom import minidom

class Design:
    """Represents a design. Contains factor and response data."""

    def __init__(self, factor_data, response_data):

        self.factor_data = factor_data
        self.response_data = response_data

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

        model_matrix = []
        for run in self.factor_data:
            model_matrix.append([])
            for term in model.terms:
                model_matrix[-1].append(term.coefficient)
                for var_id in term.powers:
                    model_matrix[-1][-1] *= run[var_id] ** term.powers[var_id]
        return model_matrix
