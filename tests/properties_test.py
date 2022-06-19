from tests.test_base import TestBase


class TestProperties(TestBase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def test_portalVersion(self):
        version = self.senertec.portalVersion
        self.assertNotEqual("", version)
