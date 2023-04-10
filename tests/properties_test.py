from test_base_test import TestBase
from datetime import datetime, timezone
from src.senertec.canipError import canipError

class TestProperties(TestBase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def test_portalVersion(self):
        version = self.senertec.portalVersion
        self.assertNotEqual("", version)

    def test_canipErrorObjectTimestamp(self):
        error = canipError()
        error.__timestamp__ = "1642621405300"
        self.assertEqual(error.timestamp, datetime(2022, 1, 19, 19, 43, 25, 300000, tzinfo=timezone.utc))
