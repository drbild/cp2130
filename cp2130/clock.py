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

from cp2130.chip import registers

class Clock(object):

    def __init__(self, chip):
        self.chip = chip

    def __repr__(self):
        return "Clock(%r)"%(self.chip)

    def __str__(self):
        return """Clock:
  divider:   %s
  frequency: %s Hz"""%(self.divider, self.frequency)

    @property
    def divider(self):
        """Get or set the clock divider configuration for the CLKOUT (GPIO.5)
        pin.

        The divider must be an integer between 1 and 256. 

        The clock frequency by the formula (24 MHz / divider). The
        clock_frequency property performs this conversion
        automatically.

        """
        divider = self.chip.get_clock_divider().clock_divider
        if divider == 0:
            divider = 256
        return divider

    @divider.setter
    def divider(self, divider):
        if not (0 < divider and divider <= 256):
            raise ValueError("Divider value must be between 1 and 256")
        if divider == 256:
            divider = 0
        reg = registers.clock_divider.make(divider)
        self.chip.set_clock_divider(reg)
        
    @property
    def frequency(self):
        """Get or set the clock frequency configuration for the CLKOUT
        (GPIO.5) pin.

        The frequency must be between 93.750 kHz and 24 MHz.

        """
        divider = self.divider
        frequency = 24000000.0 / divider
        return frequency

    @frequency.setter
    def frequency(self, frequency):
        if not (93750 <= frequency and frequency <= 24000000):
            raise ValueError("Frequency value must be between 93.75 kHz and 24 MHz")
        divider = int(24000000.0 / frequency)
        self.divider = divider
