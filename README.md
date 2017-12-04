# cp2130

[![PyPI version](https://badge.fury.io/py/cp2130.svg)](https://badge.fury.io/py/cp2130)
[![Build Status](https://travis-ci.org/drbild/cp2130.svg?branch=master)](https://travis-ci.org/drbild/cp2130)

This module provides a Python SDK for
the
[Silicon Labs CP2130 USB to SPI Bridge](https://www.silabs.com/documents/public/data-sheets/CP2130.pdf) integrated
circuit.  It exposes a Pythonic API for accessing the one-time
programmable ROM, device state, GPIOs, and SPI slave devices.

## Installation

```pip install cp2130```

The package is published to PyPI for Python 2.7 and 3.3+. `pip`
installs all dependencies.

## Dependencies

The [PyUSB](https://github.com/walac/pyusb)
or [python-libusb1](http://github.com/vpelletier/python-libusb1)
libraries is used to access the USB device. If neither `PyUSB` nor
`python-libusb1` is available for your platform, a different USB
library may be used by implementing the `cp2130.usb.USBDevice`
interface.  See `cp2130/usb/pyusb.py` and `cp2130/usb/libusb1.py` as
an examples.

## Quick-Start

The following python script illustrates basic usage of the Pythonic
API.  See
the
[CP2130 Interface Specification](https://www.silabs.com/documents/public/application-notes/AN792.pdf) for
full details of the capabilities of the chip. All features are exposed
by the API, but not all are demonstrated in this README.

```python
import cp2130
from cp2130.data import *

# If the vendor or product ids are not the default, use
# the form cp2130.find(vid=0xXXXX, pid=0xXXXX).
chip = cp2130.find() 

#######################################################
# SPI Reads/Writes
#######################################################
slave = chip.channel0

# Print a summary of the channel state
print slave

# Write 4 bytes of data to the slave
command = b'\x01\x02\x03\0x04'
slave.write(command)

# Read 8 bytes of data
response = slave.read(8)

# Issue a two-part transaction
part1 = b'\x01\x02'
part2 = b'\x03\x04'
slave.write(part1, cs_hold=True) # Keeps CS asserted
slave.write(part2)

# NOTE: cs_hold is not supported by the CP2130 native chip-select 
# capabilities. To use cs_hold, configure the chip select line as
# a GPIO instead of a chip select. This library will then manually
# manage the chip select state. I.e,:
#   chip.pin_config.gpio0.function = OutputMode.PUSH_PULL # or OutputMode.OPEN_DRAIN
# instead of
#   chip.pin_config.gpio0.function = GPIO0Mode.CS0_n

#######################################################
# GPIO Reads/Writes
#######################################################
signal = chip.gpio0

# Print a summary of the GPIO state
print signal

# Get the logic state of the pin
level = signal.value

# Set the logic state of the pin
signal.value = LogicLevel.LOW

#######################################################
# GPIO Configuration
#######################################################
# Set the mode of a GPIO
signal.mode = OutputMode.PUSH_PULL

#######################################################
# Clock Configuration
#######################################################
clock = chip.clock

# Print the clock state
print clock

# Set the clock frequency
# Use clock.divider to set the divider register directly
clock.frequency = 6 * 1000 * 1000 # 6 MHz

#######################################################
# Event Counter
#######################################################
counter = chip.event_counter

# Print a summary of the counter state 
print counter

# Get count
count = counter.count
(count, overflowed) = counter.count_with_overflow

# Set the count
counter.count = 10

# Configure the counter
counter.mode = EventCounterMode.NEGATIVE_PULSE

#######################################################
# OTP ROM Lock Byte
#######################################################
lock = c.lock

# Print a summary of the lock
print lock

# Lock the USB vendor ID
lock.vid = LockState.LOCKED

#######################################################
# OTP ROM USB Configuration
#######################################################
usb = c.usb

# Print a summary of the USB configuration
print usb

# Set the product string
usb.product_string = "ACME Widget"
c.usb = usb
print lock  # The product_string field is now locked

# Set the power mode
usb.power_mode = PowerMode.BUS_AND_REGULATOR_ON
c.usb = usb
print lock  # The power_mode field is now locked

#######################################################
# OTP ROM Pin Configuration
#######################################################
pins = c.pin_config

# Print a summary of the PIN configuration
print pins

# Print a summary of the config for one pin
print pins.gpio1
print pins.vpp

# Print the clock configuration
print pins.clock

# NOTE: The entire pin configuration must be set at one
# time.  The following example modifies several of the pins and
# then commit the entire config to the OTP ROM at once.

# Set a pin function
pins.gpio1.function = OutputMode.PUSH_PULL

# Set a pin suspend logic level
pins.miso.suspend_level = LogicLevel.HIGH
pins.miso.suspend_mode  = OutputMode.OPEN_DRAIN

# Set a pin wakeup config
pins.vpp.wakeup_level = LogicLevel.LOW
pins.vpp.wakeup_mask  = True

# Set the initial clock freqeuency
pins.clock.frequency = 6 * 1000 * 1000 # 6 MHz

# Write the config to the ROM
c.pin_config = pins
print lock # The pin_config field is now locked
```

## Library Structure

This library is organized into four distinct parts, core, data,
chip, and usb.

#### core
This component is the main high-level, Pythonic API and the one most
users will use.

It exposes the various features of the CP2130 as
objects. Configuration is done via mutable properties. Data is read
and written via methods on the objects.

#### data
This component provides enums for the fields in the CP2130
configuration.

Using explicit enums, rather than the integer encodings used in the
hardware, has two advantages.  Most importantly, it makes the code
self-documenting.  Secondly, the CP2130 uses different encodings for
some commands. The enums hides those differences.

#### chip
This component is a low-level API mirroring the native CP2130 commands. 

The `cp2130.chip` object exposes a method for command in
the
[CP2130 interface](https://www.silabs.com/documents/public/application-notes/AN792.pdf). These
methods return or take register objects defined in the
`cp2130.register` package, which expose the register fields as mutable
properties for easy access and modification.

Most users will never need to use this component directly.

#### usb
This component is an abstraction over the USB interface used to access
this CP2130.

Currently `PyUSB` and `python-libusb1` backends are supplied.

## Contributing

Please submit bugs, questions, suggestions, or (ideally) contributions
as issues and pull requests on GitHub.

### Maintainers
**David R. Bild**
+ [https://www.davidbild.org](https://www.davidbild.org)
+ [https://github.com/drbild](https://github.com/drbild)

## License
Copyright 2017 David R. Bild

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this work except in compliance with the License. You may obtain a copy of
the License from the LICENSE.txt file or at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
