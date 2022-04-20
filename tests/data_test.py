import json
import logging
import os
from unittest import TestCase
from time import sleep
from senertec.canipValue import canipValue
from senertec.client import senertec


class TestConnection(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        file = open(os.getcwd() + "\\productGroups.json")
        supportedItems = json.load(file)
        file.close()
        self.senertec = senertec(supportedItems,
                                 os.environ['SENERTECUSER'], os.environ['SENERTECPW'], level=logging.DEBUG)
        self.senertec.login()
        self.senertec.init()
        self.senertec.messagecallback = self.output

    def tearDown(self):
        self.senertec.logout()

    def test_brennstoffzellenChart(self):
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        chart = self.senertec.getChart("ChartChpActivityFCEnduser")

        self.assertTrue(chart != None)

    def test_errors(self):
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        errors = self.senertec.getErrors()
        self.assertIsNotNone(errors)

    def test_request(self):
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        for points in self.senertec.boards:
            l = points.getFullDataPointIds()
            response = self.senertec.request(l)
            self.assertTrue(response)
        sleep(3)

    def output(self, value: canipValue):
        print("Source: " + value.sourceDatapoint + "\nBoard: " +
              value.boardName + "\nName: " + value.friendlyDataName + "\nValue: " +
              value.dataValue.__str__() + value.dataUnit + "\n")
