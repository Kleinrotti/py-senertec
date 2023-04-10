from time import sleep
from test_base_test import TestBase
from src.senertec.canipValue import canipValue


class TestFunctions(TestBase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

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
        sleep(10)
        self.assertTrue(self.out.call_count > 20)
