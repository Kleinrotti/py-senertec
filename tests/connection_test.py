import json
import os
from unittest import TestCase

from src.senertec.client import senertec


class TestConnection(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        file = open(os.getcwd() + "\\productGroups.json")
        supportedItems = json.load(file)
        file.close()
        self.senertec = senertec(supportedItems,
                                 os.environ['SENERTECUSER'], os.environ['SENERTECPW'])

    def test_auth(self):
        result = self.senertec.login()
        self.assertTrue(result)

    def test_init(self):
        result = self.senertec.login()
        self.assertTrue(result)
        result = self.senertec.init()
        self.senertec.logout()
        self.assertTrue(result)

    def test_units(self):
        result = self.senertec.login()
        self.assertTrue(result)
        result = self.senertec.init()
        self.assertTrue(result)
        result = self.senertec.getUnits()
        self.senertec.logout()
        self.assertTrue(result != None)

    def test_unitConnection(self):
        result = self.senertec.login()
        self.assertTrue(result)
        result = self.senertec.init()
        self.assertTrue(result)
        serial = self.senertec.getUnits()
        self.assertTrue(serial != None)
        result = self.senertec.connectUnit(serial[0])
        self.assertTrue(result)
        result = self.senertec.disconnectUnit(serial[0])
        self.senertec.logout()
        self.assertTrue(result)
