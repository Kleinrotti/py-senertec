# py-senertec

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

The **py-senertec** library aims to provide python way to communicate with senertec dachs connect gen2.

## Requirements

*   **Python 3.6+**
*   **productGroups.json from this [repo](https://github.com/Kleinrotti/py-senertec)**
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
from senertec.client import Senertec
from senertec.canipvalue import canipvalue
import json
import os

# holds the datapoints which are fixed values parsed from Dachsportal
file = open(os.getcwd() + "\\productGroups.json")
supportedItems = json.load(file)
file.close()
senertec = Senertec(supportedItems, "username", "password")
senertec.login()
senertec.init()
#set your callback function for messages
senertec.messagecallback = self.output
```

### Requesting data

```python
serial = senertec.getUnits()
senertec.connectUnit(serial[0])
# request all available data
for points in senertec.boards:
            l = points.getFullDataPointIds()
            # result will be received through callback function which was set above
            senertec.request(l)
senertec.logout()
```

### Using callback function

Once the websocket has been started, data will be transmitted through the websocket.
In order for your to be alerted of such a change, you need to add a callback which was done above.
The callback function could look like this:

```python
def output(self, value: canipvalue):
        print(value.friendlydataname + ": " +
              value.datavalue.__str__() + value.dataunit)
```

### Errors of energy unit
Errors can also be read out with a simple function.
The errors are read out on the connect function and only will be refreshed on a reconnect.

```python
# these are returned directly from function
k = senertec.getErrors()
```