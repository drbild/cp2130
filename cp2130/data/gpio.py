# Copyright 2017 David R. Bild
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

from __future__ import absolute_import

from enum import Enum

class LogicLevel(Enum):
    """The logic level of a pin.

    """
    LOW  = 0
    HIGH = 1

    def __bool__(self):
        return True if (self == LogicLevel.HIGH) else False

    __nonzero__ = __bool__

class ChipSelectControl(Enum):
    """The chip select enable state of a pin/channel.

    """
    DISABLED          = 0
    ENABLED           = 1
    ENABLED_EXCLUSIVE = 2

class OutputMode(Enum):
    """Output mode of a pin.

    """
    OPEN_DRAIN = 0
    PUSH_PULL  = 1

class GPIOMode(Enum):
    """GPIO mode of a pin.

    """
    INPUT = 0

class GPIO0Mode(Enum):
    """Function mode of the GPIO.0 pin.

    """
    CS0_n = 0

class GPIO1Mode(Enum):
    """Function mode of the GPIO.1 pin.

    """
    CS1_n = 0

class GPIO2Mode(Enum):
    """Function mode of the GPIO.2 pin.

    """
    CS2_n = 0

class GPIO3Mode(Enum):
    """Function mode of the GPIO.3 pin.

    """
    CS3_n = 0
    RTR_n = 1
    RTR   = 2


class GPIO4Mode(Enum):
    """Function mode of the GPIO.4 pin.

    """
    CS4_n                        = 0
    EVENT_COUNTER_RISING_EDGE    = 1
    EVENT_COUNTER_FALLING_EDGE   = 2
    EVENT_COUNTER_NEGATIVE_PULSE = 3
    EVENT_COUNTER_POSITIVE_PULSE = 4


class GPIO5Mode(Enum):
    """Function mode of the GPIO.5 pin.

    """
    CS5_n  = 0
    CLKOUT = 1

class GPIO6Mode(Enum):
    """Function mode of the GPIO.6 pin.

    """
    CS6_n = 0

class GPIO7Mode(Enum):
    """Function mode of the GPIO.7 pin.

    """
    CS7_n = 0

class GPIO8Mode(Enum):
    """Function mode of the GPIO.8 pin.

    """
    CS8_n  = 0
    SPIACT = 1

class GPIO9Mode(Enum):
    """Function mode of the GPIO.9 pin.

    """
    CS9_n   = 0
    SUSPEND = 1

class GPIO10Mode(Enum):
    """Function mode of the GPIO.10 pin.

    """
    CS10_n    = 0
    SUSPEND_n = 1
