class canipValue(object):
    """Represents a data value received from websocket."""
    def __init__(self):
        self.boardName = str()
        """Name of the board."""
        self.friendlyBoardName = str()
        """Human readable name of the board."""
        self.dataValue = None
        """Value"""
        self.dataUnit = str()
        """Unit of the value."""
        self.friendlyDataName = str()
        """Human readable data value name."""
        self.sourceDatapoint = str()
        """Id of datapoint which was requested."""
