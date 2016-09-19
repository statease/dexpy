from xml.dom import minidom

def load(file_path):

    xmldoc = minidom.parse(file_path)
    factors = xmldoc.getElementsByTagName('factor')
    responses = xmldoc.getElementsByTagName('response')
    runs = xmldoc.getElementsByTagName('run')

    return Design(factors, responses, runs)

class Design:

    factors = []
    responses = []
    factor_data = []
    response_data = []

    def __init__(self, factors, responses, runs):

        self.factors = factors
        self.responses = responses

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

    @property
    def runs(self):
        return len(self.factor_data)
