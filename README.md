# py-senertec

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/py-senertec.svg)](https://badge.fury.io/py/py-senertec)

## Description

The **py-senertec** library provides a way to communicate with senertec dachsportal2 to monitor your energy unit.

## Requirements

*   **Python 3.6+**
*   **productGroups.json from [repo](https://github.com/Kleinrotti/py-senertec/blob/main/productGroups.json)**
*   **Account for Senertec Dachsportal2/Remeha KWK**

## Supported devices

For now, these devices are supported:  
*   Senertec Dachs 0.8
*   Remeha eLecta 300 (technically same as Senertec Dachs)

## Support for other devices
This library uses [Dachsportal2](https://dachsconnect.senertec.com/dachsportal2) to get information from your energy system.
If you have a device which can be accessed from Dachsportal2 adding support should be pretty easy.
You can open an feature request in the issues section and provide more information there.

## Installation

```sh
$ pip install py-senertec
```

## Usage

### Login and initialization

```python
from senertec.client import senertec
from senertec.canipvalue import canipvalue
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
serial = senertec.getUnits()
senertec.connectUnit(serial[0])
# request all available data from all boards
for points in senertec.boards:
            ids = points.getFullDataPointIds()
            # result will be received through callback function which was set above
            senertec.request(ids)
senertec.logout()
```

### Using callback function

Once the websocket has been started, data will be transmitted through the websocket.
In order for your to be alerted of such a change, you need to add a callback which was done above.
The callback function could look like this:

```python
def output(self, value: canipvalue):
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