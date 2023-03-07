import json
import logging
import os
import unittest
from unittest.mock import Mock
from src.senertec.canipValue import canipValue
from src.senertec.client import senertec


class TestBase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        # file = open(os.getcwd() + "\\productGroups.json")
        # supportedItems = json.load(file)
        # file.close()
        self.senertec = senertec(
            None, os.environ['SENERTECUSER'], os.environ['SENERTECPW'])
        self.senertec.login()
        self.senertec.init()
        self.out = Mock()
        self.senertec.messagecallback = self.out

    def tearDown(self):
        self.senertec.logout()
