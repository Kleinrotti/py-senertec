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
    # you can use the example file datapointFilter.json to fetch only datapoints you really want!
    # edit the file as your needs, this is highly recommended.
    file = open(os.getcwd() + "\\datapointFilter.json")
    filter = json.load(file)
    file.close()
    global senertec
    # set your username and password here
    senertec = senertec(filter, "username", "password", lang.German)

    # to get all possible datapoints you can specify None
    # senertec = senertec(None,"username", "password", lang.German)

    # set your callback function where received data should go to
    senertec.messagecallback = output

    # login to dachsportal2
    if senertec.login() is False:
        return
    # if login was successful you can/should initialize the platform.
    if senertec.init() is False:
        return
    # get all energy units/heating systems from your account.
    units = senertec.getUnits()
    # connect to first unit
    if senertec.connectUnit(units[0].serial) is False:
        return
    print(f"Connected to unit: {units[0].model} with serial: {units[0].serial}")
    # get errors to output them below
    errors = senertec.getErrors()
    # request datapoints. In this case all points from all boards.
    for points in senertec.boards:
        ids = points.getFullDataPointIds()
        senertec.request(ids)

    # if no datapointfilter was set above, you need to increase the sleep time a lot
    # because there are over 400 datapoints in most cases which take some time to be received
    sleep(5)
    senertec.logout()
    print("\n-----Device errors-----")
    for e in errors:
        if (e.code != ""):
            print(
                f"\nError: {e.code} in Board: {e.boardName} \nCategorie: {e.errorCategory} \nMessage: {e.errorTranslation}")

# this is the callback function to get the requested data from the websocket connection.
def output(value: canipValue):
    print("Source: " + value.sourceDatapoint + "\nName: " + value.friendlyDataName + "\nValue: " +
          value.dataValue.__str__() + value.dataUnit + "\n")


start()