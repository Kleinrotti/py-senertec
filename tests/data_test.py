import json
import os
from unittest import TestCase
from time import sleep
from src.senertec.canipvalue import canipvalue
from src.senertec.client import Senertec

class TestConnection(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        file = open(os.getcwd() + "\\productGroups.json")
        supportedItems = json.load(file)
        file.close()
        self.senertec = Senertec(supportedItems,
            os.environ['SENERTECUSER'], os.environ['SENERTECPW'])

    def test_brennstoffzellenChart(self):
        self.senertec.login()
        self.senertec.init()
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0])
        chart = self.senertec.getChart("ChartChpActivityFCEnduser")
        self.senertec.logout()
        self.assertTrue(chart != None)

    def test_request(self):
        self.senertec.login()
        self.senertec.init()
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0])
        for points in self.senertec.boards:
            l = points.getFullDataPointIds()
            response = self.senertec.request(l)
            self.assertTrue(response)
        sleep(3)
        k = self.senertec.getErrors()
        self.senertec.logout()

    def output(self, value: canipvalue):
        print(value.friendlydataname + ": " +
              value.datavalue.__str__() + value.dataunit)
