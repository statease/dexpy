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
    run_attribs = []

    def __init__(self, factors, responses, runs):

        self.factors = factors
        self.responses = responses
        self.run_attribs = runs

    @property
    def runs(self):
        return len(self.run_attribs)
