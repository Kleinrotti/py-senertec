from senertec.datapoint import datapoint


class board(object):
    def __init__(self):
        self.boardName = str()
        self.friendlyName = str()
        self.datapoints = [datapoint()]
        self.datapoints.pop()  # remove default element

    def getFullDatapoint(self, index: int):
        return self.boardName + "." + self.datapoints[index]

    def getFullDataPointIds(self):
        lst = []
        for i in self.datapoints:
            lst.append(self.boardName + "." + i.id)
        return lst
