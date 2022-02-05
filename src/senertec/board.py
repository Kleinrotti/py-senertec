from senertec.datapoint import datapoint


class board(object):
    """Represents an electronic board of the energy unit."""
    def __init__(self):
        self.boardName = str()
        """Name of the board."""
        self.friendlyName = str()
        """Human readable name of the board."""
        self.datapoints = [datapoint()]
        """Stores datapoints of the board."""
        self.datapoints.pop()  # remove default element

    def getFullDatapoint(self, index: int):
        """Get the full datapoint string."""
        return self.boardName + "." + self.datapoints[index]

    def getDatapointByName(self, name: str):
        """Get a datapoint by its name. Not case sensitive."""
        for point in self.datapoints:
            if name.lower() in point.friendlyName.lower():
                return point

    def getFullDataPointIds(self):
        """Get all datapoints."""
        lst = []
        for i in self.datapoints:
            lst.append(self.boardName + "." + i.id)
        return lst
