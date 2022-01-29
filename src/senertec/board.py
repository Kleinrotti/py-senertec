from src.senertec.datapoint import datapoint


class board(object):
    def __init__(self):
        self.boardname = str()
        self.friendlyname = str()
        self.datapoints = [datapoint()]
        self.datapoints.pop() #remove default element

    def getFullDatapoint(self, index: int):
        return self.boardname + "." + self.datapoints[index]

    def getFullDataPointIds(self):
        lst = []
        for i in self.datapoints:
            lst.append(self.boardname + "." + i.id)
        return lst
