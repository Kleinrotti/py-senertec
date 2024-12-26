from .datapoint import datapoint


class board(object):
    """Represents an electronic board of the energy unit."""

    def __init__(self):
        self.__boardName__ = str()
        """Name of the board."""
        self.__friendlyName__ = str()
        """Human readable name of the board."""
        self.__datapoints__ = [datapoint()]
        """Stores datapoints of the board."""
        self.__datapoints__.pop()  # remove default element

    @property
    def datapointCount(self) -> int:
        """Return number of datapoints."""
        return len(self.__datapoints__)

    @property
    def datapoints(self):
        """Returns all datapoints."""
        return self.__datapoints__

    @property
    def boardName(self):
        """Return the board name."""
        return self.__boardName__

    @property
    def friendlyName(self):
        """Return the human readable name of the board."""
        return self.__friendlyName__

    def getFullDatapoint(self, index: int):
        """Get the full datapoint string."""
        return self.__boardName__ + "." + self.__datapoints__[index]

    def getFullDatapointIdByName(self, name: str):
        """
        Get a full datapoint by its name. Not case sensitive.

        ``name`` Datapoint name e.g. BM001

        Returns the full datapoint as string or None if not found.
        """
        for point in self.__datapoints__:
            if name.lower() in point.sourceId.lower():
                return self.__boardName__ + "." + point.id

    def getDatapointByName(self, name: str):
        """
        Get a datapoint by its name e.g BM001. Not case sensitive.

        Returns the datapoint object or None if not found.
        """
        for point in self.__datapoints__:
            if name.lower() in point.friendlyName.lower():
                return point

    def getFullDataPointIds(self):
        """
        Get all datapoints by its full id.

        Returns a list of all datapoints as string. The first part of the string is the board identifier followed
        by a unique id which is random on each new session.
        """
        lst = []
        for i in self.__datapoints__:
            lst.append(self.__boardName__ + "." + i.id)
        return lst
