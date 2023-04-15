#
#
# This example outputs all values to the console window with a list of errors of your energy unit.
#
#
from senertec.client import senertec
from senertec.canipValue import canipValue
import json
from time import sleep
import os

result = []


def start():
    # you can use the example file datapointFilter.json to fetch only datapoints you really want!
    # edit the file as your needs, this is highly recommended.
    file = open(os.getcwd() + "\\datapointFilter.json")
    filter = json.load(file)
    file.close()
    # create a new senertec object with filter
    senertecClient = senertec(filter)
    global result
    totalDataPoints = 0
    timeoutCounter = 0

    # to get all possible datapoints you can specify None
    # senertec = senertec(None)

    # set your callback function where received data should go to
    senertecClient.messagecallback = output

    # login to dachsportal2 with email and password
    if senertecClient.login("username", "password") is False:
        return
    # if login was successful you need to initialize the platform.
    if senertecClient.init() is False:
        return
    # get all energy units/heating systems from your account.
    units = senertecClient.getUnits()
    # connect to first unit
    if senertecClient.connectUnit(units[0].serial) is False:
        return
    print(f"Connected to unit: {units[0].model} with serial: {units[0].serial}")
    # get errors to output them below
    errors = senertecClient.getErrors()

    # request all datapoints.
    for board in senertecClient.boards:
        ids = board.getFullDataPointIds()
        senertecClient.request(ids)
        totalDataPoints += len(board.datapoints)

    # if you want specific datapoints you can loop through the boards to find it and request it then
    #for board in senertecClient.boards:
    #    datapoint = board.getFullDatapointIdByName("MM011")
    #    if(datapoint):
    #        senertecClient.request(datapoint)
    #        totalDataPoints += 1
    #        break

    
    # loop wait 2 seconds and checks if all points get received
    while (len(result) < totalDataPoints):
        # break after 60sec timeout
        if timeoutCounter > 30:
            break
        sleep(2)
        timeoutCounter += 1
    # logout after all datapoints get received or timeout was reached
    senertecClient.logout()

    # print all values
    for value in result:
        print("Source: " + value.sourceDatapoint + "\nName: " + value.friendlyDataName + "\nValue: " +
              value.dataValue.__str__() + value.dataUnit + "\n")

    #print total count of received values  
    print(f"Received {len(result)} values.")

    # print all errors
    print("\n-----Device errors-----")
    for e in errors:
        if (e.code != ""):
            print(
                f"\nError: {e.code} in Board: {e.boardName} \nCategorie: {e.errorCategory} \nMessage: {e.errorTranslation}")


# this is the callback function to get the requested data from the websocket connection.
def output(value: canipValue):
    global result
    temp = next(
        (
            x
            for x in result
            if x.sourceDatapoint == value.sourceDatapoint
        ),
        None,
    )
    # sometimes we get values twice, so we filter it
    if not temp:
        result.append(value)


start()
