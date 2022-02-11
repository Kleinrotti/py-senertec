import json
import os
from unittest import TestCase
from time import sleep
from senertec.energyUnit import energyUnit
from senertec.canipValue import canipValue
from senertec.client import senertec


class TestConnection(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        file = open(os.getcwd() + "\\productGroups.json")
        supportedItems = json.load(file)
        file.close()
        self.senertec = senertec(supportedItems,
                                 os.environ['SENERTECUSER'], os.environ['SENERTECPW'])

    def test_brennstoffzellenChart(self):
        self.senertec.login()
        self.senertec.init()
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        chart = self.senertec.getChart("ChartChpActivityFCEnduser")
        self.senertec.logout()
        self.assertTrue(chart != None)

    def test_request(self):
        self.senertec.login()
        self.senertec.init()
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        for points in self.senertec.boards:
            l = points.getFullDataPointIds()
            response = self.senertec.request(l)
            self.assertTrue(response)
        sleep(3)
        self.senertec.logout()

    def output(self, value: canipValue):
        print(value.friendlyDataName + ": " +
              value.dataValue.__str__() + value.dataUnit)
