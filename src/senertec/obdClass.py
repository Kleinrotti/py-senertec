from enum import Enum


class obdClass(Enum):
    """This class defines the class/type of a datapoint."""
    Parameter = "Parameter"
    Signal = "Signal"
    Counter = "Counter"
