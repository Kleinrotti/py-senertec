# py-senertec

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/py-senertec.svg)](https://badge.fury.io/py/py-senertec)

## Description

The **py-senertec** library provides a way to communicate with Senertec Dachsportal2 to monitor your energy unit.
This library supports read-only communication. So *changing* values for your energy unit isn't implemented and not planned yet.

## Requirements

*   **Python 3.9+**
*   **Account for Senertec Dachsportal2/Remeha KWK**

## Tested with this devices

I could test with this devices but others should also work:  
*   Senertec Dachs 0.8
*   Senertec Dachs InnoGen
*   Senertec Dachs Gen2 F5.5
*   Remeha eLecta 300 (technically same as Senertec Dachs 0.8)


## Installation

```sh
$ pip install py-senertec
```

## Usage

### Login and initialization

```python
from senertec.client import senertec
from senertec.canipValue import canipValue
import json
import os

#this example uses no filtering, read below how to use a filter instead of None as first parameter.
senertec = senertec(None, "username", "password")
#set your callback function for messages
senertec.messagecallback = self.output
senertec.login()
senertec.init()
```

### Requesting data

```python
units = senertec.getUnits()
senertec.connectUnit(units[0].serial)
# request all available data from all boards
for points in senertec.boards:
            ids = points.getFullDataPointIds()
            # result will be received through callback function which was set above
            senertec.request(ids)
senertec.logout()
```

### Using callback function

Once the websocket has been started, data will be transmitted through the websocket.
To get the websocket data, you need to add a callback which was done above.
The callback function could look like this:

```python
def output(self, value: canipValue):
        print(value.friendlyDataName + ": " +
              value.dataValue.__str__() + value.dataUnit)
```

### Errors of energy unit
Errors can also be read out with a simple function.
The errors are read out on the connect function and will only be refreshed on a reconnect.

```python
# values are returned directly from function
errors = senertec.getErrors()
```

A full example can be found [here](https://github.com/Kleinrotti/py-senertec/blob/main/examples/output_data.py)

## Filtering (recommended)
If you specify a json string in the senertec contructor you can limit what datapoints should be received.
This is pretty usefull if you know what data you want from your heating system e.g. power, temperature.
By default all datapoints are included which are more than 400 in most cases and receiving them takes some time.
This json string should look like [this](https://github.com/Kleinrotti/py-senertec/blob/main/examples/datapointFilter.json).
The json string contains the productGroup at the top and below the datapoints which should be included.
You get the productGroup from the getUnits() function.

## What are these datapoints?
Take a look at this manual from [Remeha](https://mediacdn.remeha.de/-/media/websites/remehade/downloads/produkte/regenerative-hybrid/gas-hybrid-waerme-und-strom/electa-ace-300/electaace300_bedienungsanleitung_02-23.pdf?v=1&d=20230228T114400Z) (Page 39).
There is already a good explanation of how these datapoints are composed.
