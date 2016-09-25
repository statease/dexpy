

class Factor:
    """Represents a factor in a design."""

    def __init__(self, name, units, levels):

        self.name = name
        self.units = units
        self.levels = levels

    @property
    def type(self):
        """Determines the type of factor from the levels.
        TODO: This will have to be changed to a member at some point, since
        we don't want to have a O(n) cost to retrieving the type."""
        for level in self.levels:
            try:
                float(level)
            except:
                return "categoric"
        return "numeric"
