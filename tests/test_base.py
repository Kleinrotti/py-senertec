import json
import logging
import os
from unittest import TestCase
from senertec.canipValue import canipValue
from senertec.client import senertec

class TestBase(TestCase):
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

    def output(self, value: canipValue):
        pass
