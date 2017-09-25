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

from cp2130.gpio import Pin

class PinConfig(object):

    def __init__(self, register):
        self.register = register

        self.miso = PinConfig.Pin('miso', register)
        self.mosi = PinConfig.Pin('mosi', register)
        self.sck  = PinConfig.Pin('sck',  register)
        self.vpp  = PinConfig.Pin('vpp',  register)
        
        self.gpio0  = PinConfig.GPIO(0,  register) 
        self.gpio1  = PinConfig.GPIO(1,  register)
        self.gpio2  = PinConfig.GPIO(2,  register)
        self.gpio3  = PinConfig.GPIO(3,  register)
        self.gpio4  = PinConfig.GPIO(4,  register)
        self.gpio5  = PinConfig.GPIO(5,  register)
        self.gpio6  = PinConfig.GPIO(6,  register)
        self.gpio7  = PinConfig.GPIO(7,  register)
        self.gpio8  = PinConfig.GPIO(8,  register)
        self.gpio9  = PinConfig.GPIO(9,  register)
        self.gpio10 = PinConfig.GPIO(10, register)

        self.clock  = PinConfig.Clock(register)

    def __repr__(self):
        return "PinConfig(%r)"%(self.register)

    def __str__(self):
        return """PinConfig
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 %s
"""%(self.gpio0, self.gpio1, self.gpio2, self.gpio3,
     self.gpio4, self.gpio5, self.gpio6, self.gpio7,
     self.gpio8, self.gpio9, self.gpio10,
     self.miso, self.mosi, self.sck, self.vpp, self.clock)
   
    class Pin(object):

        def __init__(self, name, register):
            self.name     = name
            self.register = register

        def __repr__(self):
            return "Pin(%r, %r)"%(self.name, self.register)

        def __str__(self):
            return """%s:
  suspend_level: %s
  suspend_mode:  %s
  wakeup_mask:   %s
  wakeup_match:  %s"""%(self.name, self.suspend_level, self.suspend_mode,
                        self.wakeup_mask, self.wakeup_match)

        @property
        def suspend_level(self):
            """Get and set the suspend level of the pin as configured in the ROM.

            This method does not write to the ROM. The modified PinConfig
            instance must be applied to the chip object to write the
            value.
            
            """
            return getattr(self.register, "%s_suspend_level"%(self.name))

        @suspend_level.setter
        def suspend_level(self, suspend_level):
            setattr(self.register, "%s_suspend_level"%(self.name), suspend_level)

        @property
        def suspend_mode(self):
            """Get and set the suspend mode of the pin as configured in the ROM.
            
            This method does not write to the ROM. The modified PinConfig
            instance must be applied to the chip object to write the
            value.
            
            """
            return getattr(self.register, "%s_suspend_mode"%(self.name))

        @suspend_mode.setter
        def suspend_mode(self, suspend_mode):
            setattr(self.register, "%s_suspend_mode"%(self.name), suspend_mode)

        @property
        def wakeup_mask(self):
            """Get and set the wakeup mask of the pin as configured in the ROM.

            This method does not write to the ROM. The modified
            PinConfig instance must be applied to the chip object to
            write the value.
            
            """
            return getattr(self.register, "%s_wakeup_mask"%(self.name))

        @wakeup_mask.setter
        def wakeup_mask(self, wakeup_mask):
            setattr(self.register, "%s_wakeup_mask"%(self.name), wakeup_mask)

        @property
        def wakeup_match(self):
            """Get and set the wakeup match of the pin as configured in the ROM.

            This method does not write to the ROM. The modified
            PinConfig instance must be applied to the chip object to
            write the value.

            """
            return getattr(self.register, "%s_wakeup_match"%(self.name))

        @wakeup_match.setter
        def wakeup_match(self, wakeup_match):
            setattr(self.register, "%s_wakeup_match"%(self.name), wakeup_match)

    class GPIO(Pin):

        def __init__(self, num, register):
            super(PinConfig.GPIO, self).__init__("gpio%d"%num, register)
            self.num  = num

        def __repr__(self):
            return "GPIO(%r, %r)"%(self.num, self.register)

        def __str__(self):
            value = super(PinConfig.GPIO, self).__str__()
            return value + """
  function:      %s"""%self.function

        @property
        def function(self):
            """Get and set the function of the GPIO as configured in the ROM.

            This method does not write to the ROM. The modified
            PinConfig instance must be applied to the chip object to
            write the value.

            """

            return getattr(self.register, self.name)

        @function.setter
        def function(self, function):
            setattr(self.register, self.name, function)
         
    class Clock(object):

        def __init__(self, register):
            self.register = register

        def __repr__(self):
            return "Clock(%r)"%(self.register)

        def __str__(self):
            return """clock:
  divider:   %s
  frequency: %s Hz"""%(self.divider, self.frequency)

        @property
        def divider(self):
            """Get or set the initial clock divider for the CLKOUT (GPIO.5) pin as
            configured in the ROM.

            The divider must be an integer between 1 and 256. 

            The clock frequency by the formula (24 MHz / divider). The
            clock_frequency property performs this conversion
            automatically.

            This method does not write to the ROM. The modified
            PinConfig instance must be applied to the chip object to
            write the value.

            """
            divider = self.register.clock_divider
            if divider == 0:
                divider = 256
            return divider

        @divider.setter
        def divider(self, divider):
            if not (0 < divider and divider <= 256):
                raise ValueError("Divider value must be between 1 and 256")
            if divider == 256:
                divider = 0
            self.register.clock_divider = divider
        
        @property
        def frequency(self):
            """Get or set the initial clock frequency for the CLKOUT (GPIO.5) pin
as configured in the ROM.

            The frequency must be between 93.750 kHz and 24 MHz.

            This method does not write to the ROM. The modified
            PinConfig instance must be applied to the chip object to
            write the value.

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
