from asyncio.log import logger
import inspect
import json
import logging
from threading import Thread
import requests
import websocket
from senertec.lang import lang
from senertec.canipError import canipError
from senertec.canipValue import canipValue
from senertec.board import board
from senertec.datapoint import datapoint


class basesocketclient:
    """Base class which provides logic for a senertec websocket connection."""

    def __init__(self, level=logging.WARN):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.__is_ws_connected__ = False
        self.__messages__ = [str()]
        self.__thread__ = None
        self.__should_stop__ = False
        self.ws = None
        self.boards = [board()]
        """All available boards with datapoints which can be used in request function"""

    def __on_message__(self, ws, message):
        j = json.loads(message)
        if j["action"] == "CanipValue":
            for b in self.boards:
                if b.boardName == j["data"]["boardName"]:
                    value = canipValue()
                    value.boardName = b.boardName
                    for point in b.datapoints:
                        if point.id == j["data"]["dataPointName"]:
                            value.friendlyDataName = point.friendlyName
                            value.sourceDatapoint = point.sourceId
                            tempValue = j["data"]["value"]
                            if point.enumName != None:
                                for enum in self.__enumTranslations__:
                                    if point.enumName == enum["name"]:
                                        value.dataValue = enum["translations"][f"{tempValue}"]
                            elif point.gain != 0 and point.gain != 1:
                                value.dataValue = tempValue * \
                                    point.gain
                            else:
                                value.dataValue = tempValue
                            value.dataUnit = point.unit
                            if point.unit != None:
                                value.dataUnit = point.unit
                            else:
                                value.dataUnit = ""
                            self.messagecallback(value)
                            break
        if j["action"] == "HkaStore" and j["data"]["updateType"] == "remove":  # reconnect
            self.connectUnit(j["sn"])
        else:
            self.__messages__.append(message)

    def __on_error__(self, ws, error):
        self.logger.error(f"error : {error}")
        self.__is_ws_connected__ = False

    def __on_close__(self, ws, close_status_code, close_msg):
        self.logger.info(
            f"Connection closed to Senertec with code {close_status_code}")
        self.__is_ws_connected__ = False

    def __on_open__(self, ws):
        self.logger.info("Connected to Senertec websocket")
        self.__is_ws_connected__ = True

    def __create_websocket__(self):
        cookies = self.__getCookies__(
            self.__clientCookie__, "dachsconnect.senertec.com")
        self.ws = websocket.WebSocketApp("wss://dachsconnect.senertec.com/dachsportal2/ws",
                                         on_message=self.__on_message__,
                                         on_error=self.__on_error__,
                                         on_close=self.__on_close__,
                                         on_open=self.__on_open__,
                                         cookie=cookies)
        self.__thread__ = Thread(
            target=self.ws.run_forever, kwargs={
                "ping_interval": 60, "ping_timeout": 5}
        )
        self.__thread__.daemon = True
        self.__thread__.setName("senertec-websocket")
        self.__thread__.start()


class senertec(basesocketclient):
    """Class to communicate with Senertec and handle network calls"""

    def __init__(self, dataNames=None, email: str = None, password: str = None, language=lang.English, level=logging.INFO):
        """Constructor, create instance of senertec client.

        ``dataNames`` Json string of the productGroups.json file.

        ``language`` Set to your language.
        """
        if email is None or password is None or dataNames is None:
            raise ValueError(
                "Arguments 'email', 'passwords', dataNames are required"
            )
        super().__init__(level)
        logging.basicConfig(
            level=level,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.AUTHENTICATION_HOST = "https://dachsconnect.senertec.com/dachsportal2"
        self.email = email
        self.language = language
        self.password = password
        self.level = level
        self.__supportedItems__ = dataNames
        self.__enums__ = []
        self.__clientCookie__ = None
        self.__metaDataPoints__ = []
        self.__metaDataTranslations__ = []
        self.__enumTranslations__ = []
        self.__errorTranslations__ = []
        self.__connectedUnit__ = []
        self.messagecallback = (canipValue())
        """Set your callback function to get the data values. Function has to be overloaded with data type ``canipvalue``"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

    def __create_headers__(self):
        headers = {"Content-Type": "application/json"}
        return headers

    def __getCookies__(self, cookie_jar, domain):
        cookie_dict = cookie_jar.get_dict(domain=domain)
        found = ['%s=%s' % (name, value)
                 for (name, value) in cookie_dict.items()]
        return ';'.join(found)

    def __post__(self, urlPath: str, payload: str):
        url = self.AUTHENTICATION_HOST + urlPath
        response = requests.post(
            url, data=payload, headers=self.__create_headers__(), cookies=self.__clientCookie__)
        if(response.status_code >= 400 and response.status_code <= 599):
            logger.error("Error in post request by function: " + inspect.stack()
                         [1].function + "HTTP response: " + response.text)
        return response

    def __get__(self, urlPath: str):
        url = self.AUTHENTICATION_HOST + urlPath
        response = requests.get(
            url, headers=self.__create_headers__(), cookies=self.__clientCookie__)
        if(response.status_code >= 400 and response.status_code <= 599):
            logger.error("Error in get request by function: " + inspect.stack()
                         [1].function + "HTTP response: " + response.text)
        return response

    def __parsedatapoints__(self):
        metaData = self.__metaDataPoints__
        blist = []
        for a in metaData:
            for element in self.__supportedItems__[self.__connectedUnit__["productGroup"]]:
                if metaData[a]["friendlyName"] == element:
                    for l in self.__connectedUnit__["boards"]:
                        for o in l["attributes"]:
                            if o == metaData[a]["name"]:
                                boardname = l["name"]
                    datap = datapoint()
                    datap.sourceId = element
                    datap.id = metaData[a]["name"]
                    datap.friendlyName = self.__metaDataTranslations__[
                        metaData[a]["name"]]
                    datap.unit = metaData[a]["unit"]
                    datap.gain = metaData[a]["gain"]
                    datap.enumName = metaData[a]["enumName"]
                    # avoid doubled board entries
                    if not any(x for x in blist if x.boardName == boardname):
                        b = board()
                        b.boardName = boardname
                        b.datapoints.append(datap)
                        blist.append(b)
                    else:
                        for b in blist:
                            if b.boardName == boardname:
                                b.datapoints.append(datap)
        self.boards = blist

    def login(self):
        """
        Authenticate and get cookie.
        This function needs to be called first.
        """
        self.logger.info("Logging in...")
        response = self.__post__("/rest/info/login", json.dumps(
            {"user": self.email, "password": self.password}))
        if response.status_code == 200:
            self.__clientCookie__ = response.cookies
            return True
        else:
            return False

    def logout(self):
        """
        Logout from senertec.
        """
        self.logger.info("Logging out...")
        response = self.__get__("/logout")
        if response.status_code == 302:
            return True
        else:
            return False

    def init(self):
        """
        Initialize Senertec platform and connect to websocket.
        This function needs to be called after login.
        """
        self.logger.info("Initializing senertec platform...")
        response = self.__get__("/rest/info/init")
        if response.status_code == 200:
            self.__create_websocket__()
            j = json.loads(response.text)
            self.__metaDataPoints__ = j["metaDataPoints"]
            self.__enums__ = j["enums"]
            self.__enumTranslations__ = j["translations"][f"{self.language.value}"]["enums"]
            self.__metaDataTranslations__ = j["translations"][
                f"{self.language.value}"]["metaDataPoints"]["translations"]
            self.__errorTranslations__ = j["translations"][f"{self.language.value}"]["errorCategories"]
            return True
        else:
            return False

    def getUnits(self):
        """
        Get all units.
        This function receives all senertec products of this account.
        """
        response = self.__post__(
            "/rest/info/units", json.dumps({"limit": 10, "offset": 0, "filter": {}}))
        if response.status_code == 200:
            values = json.loads(response.text)
            units = []
            for x in values["units"]:
                units.append(
                    {"name": x["benennung"], "serial": x["seriennummer"]})
            return units
        else:
            return None

    def connectUnit(self, serial: str):
        """
        Connect to a unit.
        This function connects to a unit and enables receiving data for that unit.

        ``serial`` Serial number of energy unit. Can be received with getUnits() method.
        """
        response = self.__get__(f"/rest/canip/{serial}")
        if response.status_code == 200:
            self.__connectedUnit__ = json.loads(response.text)
            self.__parsedatapoints__()
            return True
        else:
            return False

    def disconnectUnit(self):
        """
        Disconnect from a unit.
        This function disconnects from a unit.
        """
        sn = self.__connectedUnit__["seriennummer"]
        response = self.__get__(f"/rest/canip/{sn}/disconnect")
        if response.status_code == 200:
            return True
        else:
            return False

    def getChart(self, chartname: str):
        """
        Get a history chart of the connected unit.
        """
        sn = self.__connectedUnit__["seriennummer"]
        response = self.__post__(
            f"/rest/charts/{sn}/data", json.dumps(
                {"start": 1641596400000, "end": None, "parameters": {}, "chartName": chartname, "sn": sn}))
        if response.status_code == 200:
            return json.loads(response.text)

    def request(self, dataPoints: list):
        """
        Request data from specific data points of the connected unit.
        Data received through websocket.

        ``dataPoints`` List of datapoint strings
        """
        sn = self.__connectedUnit__["seriennummer"]
        response = self.__post__(
            f"/rest/canip/{sn}/request", json.dumps(
                {"seriennummer": sn, "keys": dataPoints}))
        result = json.loads(response.text)
        if response.status_code == 200 and result["success"] and not result["errorKeys"]:
            return True
        else:
            return False

    def getBoardList(self):
        """Get all boards of the connected unit"""
        lst = [str()]
        for b in self.__connectedUnit__["boards"]:
            lst.append(b["name"])
        return lst

    def getErrors(self, onlyCurrentErrors: bool = True):
        """Get an error history of the connected unit. This gets loaded when a unit gets connected."""
        lst = [canipError]
        for b in self.__connectedUnit__["boards"]:
            for e in b["canipErrors"]:
                if onlyCurrentErrors and not e["currentError"]:
                    continue
                error = canipError()
                error.boardName = e["boardName"]
                error.code = e["codeText"]
                error.counter = e["counter"]
                error.currentError = e["currentError"]
                error.timestamp = e["timestamp"]
                cat = e["errorCode"]["category"]
                code = e["errorCode"]["code"]
                error.errorCategory = self.__errorTranslations__[
                    f"{cat}"]["translationMedium"]
                error.errorTranslation = self.__errorTranslations__[
                    f"{cat}"]["translations"][f"{code}"]
                lst.append(error)
        return lst
