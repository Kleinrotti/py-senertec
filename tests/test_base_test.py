import os
import unittest
from unittest.mock import Mock
from src.senertec.client import senertec


class TestBase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        self.senertec = senertec()
        self.senertec.login(
            os.environ['SENERTECUSER'], os.environ['SENERTECPW'])
        self.senertec.init()
        self.out = Mock()

    def tearDown(self):
        self.senertec.logout()
