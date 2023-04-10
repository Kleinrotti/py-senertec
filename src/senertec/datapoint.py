from .obdClass import obdClass


class datapoint(object):
    """Represents a datapoint of a board."""
    def __init__(self):
        self.id = str()
        """Unique datapoint id. This id is random and changes every session."""
        self.sourceId = str()
        """Name of the datapoint e.g. BM001."""
        self.friendlyName = str()
        """Human readable name of the datapoint."""
        self.unit = str()
        """Unit of the datapoint."""
        self.gain = int()
        """Scaling of interger or float values."""
        self.enumName = str()
        """If the datapoint is an enum, this value is set."""
        self.type = obdClass
        """The datapoint obdClass."""
        self.array = bool
        """Indicates if this datapoint is an array."""