# py-senertec

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/py-senertec.svg)](https://badge.fury.io/py/py-senertec)

## Description

The **py-senertec** library provides a way to communicate with Senertec Dachsportal2 to monitor your energy unit.
This library supports read-only communication currently. So *changing* values for your energy unit isn't implemented.

## Requirements

*   **Python 3.6+**
*   **productGroups.json included in this [repo](https://github.com/Kleinrotti/py-senertec/blob/main/productGroups.json)**
*   **Account for Senertec Dachsportal2/Remeha KWK**

## Supported devices

For now, these devices are supported:  
*   Senertec Dachs 0.8
*   Senertec Dachs Gen2 F5.5
*   Remeha eLecta 300 (technically same as Senertec Dachs 0.8)

## Support for other devices
This library uses [Dachsportal2](https://dachsconnect.senertec.com/dachsportal2) to get information from your energy system.
If you have a device which can be accessed from Dachsportal2 adding support should be pretty easy.
You can open a feature request in the issues section and provide more information there.

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

# holds the datapoints which are fixed values parsed from Dachsportal
file = open(os.getcwd() + "\\productGroups.json")
supportedItems = json.load(file)
file.close()
senertec = senertec(supportedItems, "username", "password")
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
The errors are read out on the connect function and only will be refreshed on a reconnect.

```python
# values are returned directly from function
k = senertec.getErrors()
```