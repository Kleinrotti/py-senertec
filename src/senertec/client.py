from asyncio.log import logger
import inspect
import json
import logging
from threading import Thread
import requests
import websocket
from bs4 import BeautifulSoup
from .energyUnit import energyUnit
from .lang import lang
from .canipError import canipError
from .canipValue import canipValue
from .board import board
from .datapoint import datapoint


class basesocketclient:
    """Base class which provides logic for a senertec websocket connection."""

    def __init__(self, level=logging.WARN):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.WS_HOST = "wss://dachsconnect.senertec.com/ws"
        self.__is_ws_connected__ = False
        self.__messages__ = [str()]
        self.__thread__ = None
        self.ws = None
        self.boards = [board()]
        """All available boards with datapoints which can be used in request function"""

    def __on_message__(self, ws, message):
        j = json.loads(message)
        action = j["action"]
        data = j["data"]
        if action == "CanipValue":
            self.logger.debug("Received new CanipValue from websocket.")
            for b in self.boards:
                if b.boardName == data["boardName"]:
                    value = canipValue()
                    value.boardName = b.boardName
                    for point in b.datapoints:
                        if point.id == data["dataPointName"]:
                            value.friendlyDataName = point.friendlyName
                            value.sourceDatapoint = point.sourceId
                            tempValue = data["value"]
                            if point.enumName != None:
                                for enum in self.__enumTranslations__:
                                    if point.enumName == enum["name"]:
                                        try:
                                            value.dataValue = enum["translations"][f"{tempValue}"]
                                        except KeyError:
                                            self.logger.warning(
                                                f"No enum translation found for datapoint '{point.friendlyName}'.")
                                            value.dataValue = "Unknown"
                            elif point.gain != 0 and point.gain != 1:
                                value.dataValue = tempValue * \
                                    point.gain
                            else:
                                value.dataValue = tempValue
                            if point.unit != None:
                                value.dataUnit = point.unit
                            else:
                                value.dataUnit = ""
                            self.messagecallback(value)
                            break
        elif action == "HkaStore" and data["updateType"] == "remove":
            sn = j["sn"]
            self.logger.info(
                f"Unit with serial {sn} got disconnected.")
        else:
            self.logger.debug(f"Received new websocket message {action}.")
            self.__messages__.append(message)

    def __on_error__(self, ws, error):
        self.logger.error(f"error : {error}")

    def __on_close__(self, ws, close_status_code, close_msg):
        self.logger.info(
            f"Senertec Websocket closed with code {close_status_code}")
        self.__is_ws_connected__ = False

    def __on_open__(self, ws):
        self.logger.info("Connected to Senertec websocket")
        self.__is_ws_connected__ = True

    def __create_websocket__(self):
        cookies = self.__getCookies__(
            self.__session__.cookies, "dachsconnect.senertec.com")
        self.logger.debug("Creating websocket connection..")
        self.ws = websocket.WebSocketApp(self.WS_HOST,
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
        self.logger.debug("Websocket connection started.")


class senertec(basesocketclient):
    """Class to communicate with Senertec and handle network calls"""

    def __init__(self, datapointList=None, email: str = None, password: str = None, language=lang.English, level=logging.INFO):
        """Constructor, create instance of senertec client.

        ``datapointList`` Json string to add only these datapoints instead of everything.

        ``language`` Set to your language.
        """
        if email is None or password is None:
            raise ValueError(
                "Arguments 'email', 'passwords'"
            )
        super().__init__(level)
        logging.basicConfig(
            level=level,
            format='py-senertec: %(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.AUTHENTICATION_HOST = "https://dachsconnect.senertec.com"
        self.SSO_HOST = "https://sso-portal.senertec.com"
        self.email = email
        self.__session__ = None
        self.language = language
        self.password = password
        self.level = level
        self.__filteredDatapoints__ = datapointList
        self.__enums__ = []
        self.__metaDataPoints__ = []
        self.__metaDataTranslations__ = []
        self.__enumTranslations__ = []
        self.__errorTranslations__ = []
        self.__connectedUnit__ = []
        self.__appVersion__ = ""
        self.messagecallback = (canipValue())
        """Set your callback function to get the data values. Function has to be overloaded with data type ``canipValue``"""
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
        response = self.__session__.post(
            url, data=payload, headers=self.__create_headers__())
        if (response.status_code >= 400 and response.status_code <= 599):
            logger.error("Error in post request by function: " + inspect.stack()
                         [1].function + " HTTP response: " + response.text)
        return response

    def __get__(self, urlPath: str):
        url = self.AUTHENTICATION_HOST + urlPath
        response = self.__session__.get(
            url, headers=self.__create_headers__())
        if (response.status_code >= 400 and response.status_code <= 599):
            logger.error("Error in get request by function: {" + inspect.stack()
                         [1].function + "} HTTP response: " + response.text)
        return response

    def __parseDataPoints__(self):
        """Parse all available datapoints for connected unit."""
        self.logger.debug("Starting to parse datapoints..")
        dataPointCount = 0
        metaData = self.__metaDataPoints__
        allPoints = []
        boardList = []

        # first collect all available datapoints
        for point in metaData:
            if metaData[point]["friendlyName"] is not None:
                datap = datapoint()
                datap.sourceId = metaData[point]["friendlyName"]
                datap.friendlyName = self.__metaDataTranslations__[
                    metaData[point]["name"]]
                datap.id = metaData[point]["name"]
                datap.gain = metaData[point]["gain"]
                datap.unit = metaData[point]["unit"]
                datap.enumName = metaData[point]["enumName"]
                allPoints.append(datap)
                # loop through all boards of unit
                for b in self.__connectedUnit__["boards"]:
                    # add board to the collection if its not already included
                    if not any(x for x in boardList if x.boardName == b["name"]):
                        device = board()
                        device.boardName = b["name"]
                        boardList.append(device)
                    # loop through datapoints of that board and add available points
                    for at in b["attributes"]:
                        if at == datap.id:
                            for b1 in boardList:
                                if b1.boardName == b["name"]:
                                    dataPointCount += 1
                                    b1.datapoints.append(datap)
                            break
        self.logger.debug(
            f"Finished datapoints parsing. Found {len(boardList)} boards with {dataPointCount} datapoints in total.")
        self.boards = boardList
        return

    def __parseDataPointsFiltered__(self):
        """Use this function to include only datapoints of datapointList which was set in class constructor."""
        self.logger.debug("Starting to parse datapoints..")
        metaData = self.__metaDataPoints__
        blist = []
        dataPointCount = 0
        boardname = ""
        for a in metaData:
            for element in self.__filteredDatapoints__[self.__connectedUnit__["productGroup"]]:
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
                    dataPointCount += 1
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
        self.logger.debug(
            f"Finished datapoints parsing. Found {len(blist)} boards with {dataPointCount} datapoints in total.")

    @property
    def portalVersion(self) -> str:
        """Returns Senertec Dachsportal version.

        Init function has to be called first.
        """
        return self.__appVersion__

    def login(self):
        """
        Login.

        This function needs to be called first.

        Returns True on success, False on failure.
        """
        self.logger.info("Logging in..")
        self.__session__ = requests.Session()
        loginSSOResponse = self.__session__.get(
            self.AUTHENTICATION_HOST + "/rest/saml2/login")

        authState = loginSSOResponse.url.split("loginuserpass.php?")[1]
        head = {"Content-Type": "application/x-www-form-urlencoded"}
        userData = f"username={self.email}&password={self.password}&{authState}"
        # submit credentials
        loginResponse = self.__session__.post(self.SSO_HOST + "/simplesaml/module.php/core/loginuserpass.php?",
                                              data=userData, headers=head)

        # filter out samlresponse and relaystate for ACS request
        soup = BeautifulSoup(loginResponse.text, features="html.parser")
        try:
            samlResponse = soup.findAll(
                "input", {"name": "SAMLResponse"})[0]["value"]
            relayState = soup.findAll(
                "input", {"name": "RelayState"})[0]["value"]
        except IndexError:
            self.logger.error("Login failed, username or password wrong.")
            return False
        acsData = {'SAMLResponse': {samlResponse}, 'RelayState': {relayState}}

        # do assertion consumer service request with received saml response
        acs = self.__session__.post(
            self.AUTHENTICATION_HOST + "/rest/saml2/acs", data=acsData, headers=head)

        if acs.history[0].status_code != 302:
            self.logger.error("Login failed at ACS request, got no redirect.")
            return False
        self.logger.info("Login was successful.")
        return True

    def logout(self):
        """
        Logout from senertec.

        Returns True on success, False on failure.
        """
        self.logger.info("Logging out..")
        response = self.__get__("/logout")
        if self.ws:
            self.ws.close()
        self.__session__.close()
        if response.status_code == 200:
            self.logger.debug("Logout was successful.")
            return True
        else:
            return False

    def init(self):
        """
        Initialize Senertec platform and connect to websocket.

        This function needs to be called after login.

        Returns True on success, False on failure.
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
            self.__appVersion__ = j["app"]["version"]
            return True
        else:
            return False

    def getUnits(self) -> list[energyUnit]:
        """
        Get all units.

        Returns all energy units of this account as object list.
        """
        response = self.__post__(
            "/rest/info/units", json.dumps({"limit": 10, "offset": 0, "filter": {}}))
        if response.status_code == 200:
            values = json.loads(response.text)
            units = []
            for x in values["units"]:
                unit = energyUnit()
                unit.model = x["benennung"]
                unit.serial = x["seriennummer"]
                unit.connected = x["connected"]
                unit.online = x["online"]
                unit.itemNumber = x["artikelNummer"]
                unit.contact = x["standortAnsprech"]
                unit.city = x["standortOrt"]
                unit.locationName = x["standortName"]
                unit.postalCode = x["standortPlz"]
                unit.street = x["standortAdresse"]
                unit.productGroup = x["productGroup"]
                units.append(unit)
            self.logger.debug(
                f"Successful received a list of {len(units)} units.")
            return units
        else:
            return None

    def connectUnit(self, serial: str):
        """
        This function connects to a unit and enables receiving data for that unit.

        ``serial`` Serial number of energy unit. Can be received with getUnits() method.

        Returns True on success, False on failure.
        """
        response = self.__get__(f"/rest/canip/{serial}")
        if response.status_code == 200:
            self.__connectedUnit__ = json.loads(response.text)
            # if no supported items were set in constructor, do not filter and parse every datapoint
            if self.__filteredDatapoints__ is None:
                self.__parseDataPoints__()
            else:
                self.__parseDataPointsFiltered__()
            return True
        else:
            return False

    def disconnectUnit(self):
        """
        Disconnect from a unit.

        Returns True on success, False on failure.
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
        Request data from specific datapoints of the connected unit.

        Data wil be received through websocket.

        ``dataPoints`` List of datapoint strings

        Returns True on success, False on failure.
        """
        sn = self.__connectedUnit__["seriennummer"]
        j = json.dumps(
            {"seriennummer": sn, "keys": dataPoints})
        response = self.__post__(
            f"/rest/canip/{sn}/request", j)
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

    def getErrors(self, onlyCurrentErrors: bool = True) -> list[canipError]:
        """Get an error history of the connected unit.

        ``onlyCurrentErrors`` Return only errors which are present now. Set to false if you want error history.

        This gets loaded when a unit gets connected."""
        lst = []
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
