#
#
# This example outputs all values to the console window with a list of errors of your energy unit.
#
#

from senertec.lang import lang
from senertec.client import senertec
from senertec.canipValue import canipValue
import json
from time import sleep
import os


def start():
    #you can use the productGroups.json to use only these datapoints and not every datapoint found!
    #file = open(os.getcwd() + "\\productGroups.json")
    #supportedItems = json.load(file)
    #file.close()
    global senertec
    #set your username and password here
    #senertec = senertec(supportedItems,"username", "password", lang.German)
    senertec = senertec(None,"username", "password", lang.German)
    senertec.messagecallback = output
    if senertec.login() is False:
        return
    if senertec.init() is False:
        return
    serial = senertec.getUnits()
    #connect to first unit
    if senertec.connectUnit(serial[0].serial) is False:
        return
    errors = senertec.getErrors()
    for points in senertec.boards:
        ids = points.getFullDataPointIds()
        senertec.request(ids)
    sleep(3)
    senertec.logout()
    print("\n-----Device errors-----")
    for e in errors:
        if(e.code != ""):
            print(
                f"\nError: {e.code} in Board: {e.boardName} \nCategorie: {e.errorCategory} \nMessage: {e.errorTranslation}")


def output(value: canipValue):
    print("Source: " + value.sourceDatapoint + "\nName: " + value.friendlyDataName + "\nValue: " +
              value.dataValue.__str__() + value.dataUnit + "\n")


start()