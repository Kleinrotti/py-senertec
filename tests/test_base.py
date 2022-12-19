import json
import logging
import os
import unittest
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
from src.senertec.canipValue import canipValue
from src.senertec.client import senertec


class TestBase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        file = open(os.getcwd() + "\\productGroups.json")
        supportedItems = json.load(file)
        file.close()
        self.senertec = senertec(supportedItems,os.environ['SENERTECUSER'], os.environ['SENERTECPW'], level=logging.DEBUG)
        self.senertec.login()
        self.senertec.init()
        self.senertec.messagecallback = self.output

    def tearDown(self):
        self.senertec.logout()

    def output(self, value: canipValue):
        pass

if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
