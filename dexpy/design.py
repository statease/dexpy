from xml.dom import minidom

class Design:
    """Represents a design. Contains factor and response data."""

    def __init__(self, factors, responses, runs):

        self.factors = factors
        self.responses = responses
        self.factor_data = []
        self.response_data = []

        for r_ele in runs:
            factor_settings = []
            for fac_actual in r_ele.getElementsByTagName('facActual'):
                factor_settings.append(fac_actual.firstChild.nodeValue)
            self.factor_data.append(factor_settings)

            response_values = []
            for res_val in r_ele.getElementsByTagName('resVal'):
                if res_val.firstChild.nodeValue == "Missing":
                    response_values.append(None)
                else:
                    response_values.append(res_val.firstChild.nodeValue)
            self.response_data.append(response_values)

    @classmethod
    def load(cls, file_path):
        "Loads an xml file into a Design object."

        xmldoc = minidom.parse(file_path)
        factors = xmldoc.getElementsByTagName('factor')
        responses = xmldoc.getElementsByTagName('response')
        runs = xmldoc.getElementsByTagName('run')

        return cls(factors, responses, runs)

    @property
    def runs(self):
        "Returns the number of runs in the design."
        return len(self.factor_data)
