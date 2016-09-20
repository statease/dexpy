import re
import string

class Term:
    """An individual term in a model."""
    _i_index = 8
    _valid_vars = string.ascii_uppercase.replace("I", "")

    def __init__(self, coefficient, powers):
        self.coefficient = float(coefficient)
        self.powers = powers

    def __str__(self):
        out = ""
        if self.coefficient != 1:
            out += str(self.coefficient)
        for var_id in self.powers:
            power = self.powers[var_id]
            if power != 0:
                out += self._valid_vars[var_id % len(self._valid_vars)]
                if var_id >= len(self._valid_vars) * 2:
                    out += '"'
                elif var_id >= len(self._valid_vars):
                    out += "'"
                if power != 1:
                    out += "^" + str(power)
        return out

    @classmethod
    def from_string(cls, term_string):

        coefficient = 1.0
        term_string = term_string.strip()
        m = re.search('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?', term_string)
        if m:
            coefficient = m.group(0)

        p = re.compile('([a-zA-Z])([\'\"]?)(?:\^(\d+))?')
        iterator = p.finditer(term_string)
        powers = {}
        for match in iterator:

            var = match.group(1).upper()
            var_id = cls._valid_vars.find(var)
            if var_id == -1:
                raise RuntimeError("Invalid variable name used: '{}'".format(var))

            # check for prime/double-prime notation
            if match.group(2) == "'":
                var_id += len(cls._valid_vars) # skip the first 25 variable ids (A to Z minus I)
            elif match.group(2) == '"':
                var_id += len(cls._valid_vars) * 2 # skip A to Z and A' to Z'

            power = 1
            if match.group(3):
                power = int(match.group(3))
            powers[var_id] = power

        return cls(coefficient, powers)


class LinearModel:
    """Represents a linear regression model."""

    def __init__(self, terms):
        self.terms = terms

    def __str__(self):
        out = []
        for term in self.terms:
            out.append(str(term))
        return " + ".join(out)

    @classmethod
    def from_string(cls, model_string):
        return cls(LinearModel.parse_terms(model_string))

    @staticmethod
    def parse_terms(model_string):
        terms = []
        for t in model_string.split("+"):
            terms.append(Term.from_string(t))
        return terms
