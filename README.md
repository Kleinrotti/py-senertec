# py-senertec

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/py-senertec.svg)](https://badge.fury.io/py/py-senertec)

## Description

The **py-senertec** library provides a way to communicate with Senertec Dachsportal2 to monitor your energy unit.
This library supports read-only communication. So _changing_ values for your energy unit isn't implemented and not planned.

## Requirements

- **Python >=3.10**
- **Account for Senertec Dachsportal2/Remeha KWK**

## Tested with these devices

I could test with these devices but others should also work:

- Senertec Dachs 0.8
- Senertec Dachs InnoGen
- Senertec Dachs Gen2 F5.5
- Remeha eLecta 300 (technically same as Senertec Dachs 0.8)

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

# Initialize class
client = senertec()
# set your callback function for messages
client.messagecallback = self.output
# login
client.login("username", "password")
client.init()
```

### Set the callback function

Once the websocket has been started, data will be transmitted through the websocket.
To get the websocket data, you need to add a callback which was done above.
The callback function could look like this:

```python
def output(self, value: canipValue):
        print(value.friendlyDataName + ": " +
              value.dataValue.__str__() + value.dataUnit)
```

### Requesting data

```python
units = client.getUnits()
# connect to first unit in the list
client.connectUnit(units[0].serial)
# request all available datapoints from all boards
# This should only be used for testing, it recommended to use a filter instead
# Take a look in the examples folder for a detailed example.
client.request(None)
# logout when you're finished
client.logout()
# or disconnect if you want to connect to another unit afterwards
# client.disconnectUnit()
```

### Errors of energy unit

Errors can also be read out with a simple function.
The errors are read out on the connect function and will only be refreshed on a reconnect.

```python
# values are returned directly from function
errors = client.getErrors()
```

### The full example can be found [here](https://github.com/Kleinrotti/py-senertec/blob/main/examples/output_data.py)

## Filtering (recommended)

If you specify a json string in the request() function you can limit what datapoints should be received.
This is recommended if you know what data you want from your heating system e.g. power, temperature.
By default all datapoints are included which are more than 400 in most cases and receiving them takes some time and
sometimes not every value will be received.
This json string should look like [this](https://github.com/Kleinrotti/py-senertec/blob/main/examples/datapointFilter.json).
The json string contains the productGroup at the top and below the datapoints which should be included.
You get the productGroup name from the getUnits() function.

You can also optionally include the boardname for a datapoint in the json.
This is usefull if a datapoint exists in multiple boards but you only want e.g. AM027 from board SCB-04@1.

## What are these datapoints?

Take a look at this manual from [Remeha](https://mediacdn.remeha.de/-/media/websites/remehade/downloads/produkte/regenerative-hybrid/gas-hybrid-waerme-und-strom/electa-ace-300/electaace300_bedienungsanleitung_02-23.pdf?v=1&d=20230228T114400Z) (Page 39).
There is already a good explanation of how these datapoints are composed.
