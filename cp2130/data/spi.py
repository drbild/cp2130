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

from bidict import bidict
from enum import Enum

class ClockPhase(Enum):
    """SPI clock phase.

    """
    LEADING_EDGE  = 0
    TRAILING_EDGE = 1

class ClockPolarity(Enum):
    """SPI clock polarity.

    """
    IDLE_LOW  = 0
    IDLE_HIGH = 1

class SPIMode(object):

    def __init__(self, mode, polarity, phase):
        self.mode           = mode
        self.clock_polarity = polarity
        self.clock_phase    = phase

    def __str__(self):
        return "SPI Mode %s"%self.mode

    def __repr__(self):
        return "SPIMode(%r, %r, %r)"%(self.mode, self.clock_polarity, self.clock_phase)

    @staticmethod
    def of(polarity, phase):
        for mode in [SPIMode.MODE_0, SPIMode.MODE_1, SPIMode.MODE_2, SPIMode.MODE_3]:
            if mode.clock_polarity == polarity and mode.clock_phase == phase:
                return mode
        raise ValueError("(%s, %s) are not a valid clock polarity and phase.")

SPIMode.MODE_0 = SPIMode(0, ClockPolarity.IDLE_LOW,  ClockPhase.LEADING_EDGE)
SPIMode.MODE_1 = SPIMode(1, ClockPolarity.IDLE_LOW,  ClockPhase.TRAILING_EDGE)
SPIMode.MODE_2 = SPIMode(2, ClockPolarity.IDLE_HIGH, ClockPhase.LEADING_EDGE)
SPIMode.MODE_3 = SPIMode(3, ClockPolarity.IDLE_HIGH, ClockPhase.TRAILING_EDGE)
