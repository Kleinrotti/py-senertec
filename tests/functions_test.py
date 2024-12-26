import os
from time import sleep
from test_base_test import TestBase
from src.senertec.canipValue import canipValue
from src.senertec.obdClass import obdClass
import json


class TestFunctions(TestBase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.counter = 0
        self.result = []
        self.totalDataPoints = 0
        self.timeoutCounter = 0

    def wait_and_print(self):
        self.timeoutCounter = 0
        # loop waits 2 second and checks if all points get received
        while (self.counter < self.totalDataPoints):
            # break after 60sec timeout
            if self.timeoutCounter > 30:
                print("Timeout reached")
                break
            sleep(2)
            self.timeoutCounter += 1
        # print all values
        self.printValues()
        self.assertTrue(self.out.call_count >= self.totalDataPoints)

    def test_brennstoffzellenChart(self):
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        chart = self.senertec.getChart("ChartChpActivityFCEnduser")
        self.assertTrue(chart is not None)

    def test_errors(self):
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        errors = self.senertec.getErrors()
        self.assertIsNotNone(errors)

    def test_request_single(self):
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        self.totalDataPoints = self.senertec.request("AM027")
        self.assertGreater(self.totalDataPoints, 0)
        self.wait_and_print()

    def test_request_list(self):
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        self.totalDataPoints = self.senertec.request(
            ["IM028", "BM001", "FM049", "FM020"])
        self.assertGreater(self.totalDataPoints, 0)
        self.wait_and_print()

    def test_request_dict(self):
        file = open(os.getcwd() + "\\examples\\datapointFilter.json")
        filter = json.load(file)
        file.close()
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        self.totalDataPoints = self.senertec.request(filter)
        self.assertGreater(self.totalDataPoints, 0)
        self.wait_and_print()

    def test_request_all(self):
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        self.totalDataPoints = self.senertec.request(None)
        self.assertGreater(self.totalDataPoints, 0)
        self.wait_and_print()

    def test_request_by_type(self):
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        self.totalDataPoints = self.senertec.request_by_type(obdClass.Counter)
        self.assertGreater(self.totalDataPoints, 0)
        self.wait_and_print()

    def test_request_with_board(self):
        self.senertec.messagecallback = self.output
        serial = self.senertec.getUnits()
        self.senertec.connectUnit(serial[0].serial)
        self.totalDataPoints = self.senertec.request_with_board(
            "AM027", "SCB-04@1")
        self.assertGreater(self.totalDataPoints, 0)
        self.wait_and_print()

    def printValues(self):
        for value in self.result:
            print("\nSource: " + value.sourceDatapoint + "\nBoard: " + value.boardName + "\nName: " + value.friendlyDataName + "\nValue: " +
                  value.dataValue.__str__() + value.dataUnit)

        print(f"Total count: {self.counter} from {self.totalDataPoints}")

    def output(self, value: canipValue):
        temp = next(
            (
                x
                for x in self.result
                if x.sourceDatapoint == value.sourceDatapoint
            ),
            None,
        )
        # sometimes we get values twice, so we filter it
        if not temp:
            self.counter = self.counter + 1
            self.result.append(value)
            # call mock method
            self.out()
