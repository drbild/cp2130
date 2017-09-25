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

class Pin(object):

    def __init__(self, name, chip):
        self.name = name
        self.chip = chip

    def __repr__(self):
        return "Pin(%r, %r)"%(self.name, self.chip)

    def __str__(self):
        return """%s:
  suspend_level: %s
  suspend_mode:  %s
  wakeup_mask:   %s
  wakeup_match:  %s"""%(self.name,
                        self.suspend_level, self.suspend_mode,
                        self.wakeup_mask, self.wakeup_match)

    @property
    def suspend_level(self):
        """Get the suspend level of the pin as configured in the ROM.

        This property is read-only.  It may be set via the pin_config
        property of the chip.

        """
        reg = self.chip.get_pin_config()
        return getattr(reg, "%s_suspend_level"%(self.name))

    @property
    def suspend_mode(self):
        """Get the suspend mode of the pin as configured in the ROM.

        This property is read-only.  It may be set via the pin_config
        property of the chip.

        """
        reg = self.chip.get_pin_config()
        return getattr(reg, "%s_suspend_mode"%(self.name))

    @property
    def wakeup_mask(self):
        """Get the wakeup mask of the pin as configured in the ROM.

        This property is read-only.  It may be set via the pin_config
        property of the chip.

        """
        reg = self.chip.get_pin_config()
        return getattr(reg, "%s_wakeup_mask"%(self.name))

    @property
    def wakeup_match(self):
        """Get the wakeup match of the pin as configured in the ROM.

        This property is read-only.  It may be set via the pin_config
        property of the chip.

        """
        reg = self.chip.get_pin_config()
        return getattr(reg, "%s_wakeup_match"%(self.name))
    
class GPIO(Pin):

    def __init__(self, num, chip):
        super(GPIO, self).__init__("gpio%d"%num, chip)
        self.num  = num

    def __repr__(self):
        return "GPIO(%r, %r)"%(self.num, self.chip)

    def __str__(self):
        value = super(GPIO, self).__str__()
        return value + \
"""
  function:      %s
  mode:          %s
  level:         %s
  value:         %s"""%(self.function, self.mode, self.level, self.value)


    @property
    def function(self):
        """Get the function of the GPIO as configured in the ROM.

        This property is read-only.  It may be set via the pin_config
        property of the chip.

        """
        reg = self.chip.get_pin_config()
        return getattr(reg, self.name)

    @property
    def mode_and_level(self):
        """Get or set the mode and level of the GPIO. The pin function must be
        configured as an output to set the level.

        """
        reg   = self.chip.get_gpio_mode_and_level()
        mode  = reg.mode(self.num)
        level = reg.level(self.num)
        return (mode, level)

    @mode_and_level.setter
    def mode_and_level(self, mode_and_level):
        (mode, level) = mode_and_level
        reg = registers.one_gpio_mode_and_level.make(mode, level)
        self.chip.set_gpio_mode_and_level(self.num, reg)
    
    @property
    def mode(self):
        """Get or set the mode of the GPIO.

        """
        (mode, _) = self.mode_and_level
        return mode

    @mode.setter
    def mode(self, mode):
        level = self.level
        self.mode_and_level = (mode, level)

    @property
    def level(self):
        """Get or set the level of the GPIO. The pin must be configured as an
        output.

        The property should be equivalent to the :value: property.

        """
        (_, level) = self.mode_and_level
        return level

    @level.setter
    def level(self, level):
        mode = self.mode
        self.mode_and_level = (mode, level)

    @property
    def value(self):
        """Get or set the value of the GPIO. The pin must be configured as an
        output.
        
        This property should be equivalent to the :level: property.

        """
        reg = self.chip.get_gpio_values()
        return reg.level(self.num)

    @value.setter
    def value(self, value):
        self.level = value

    @property
    def cs_enable(self):
        """Get or set the chip select enable state of the GPIO.

        """
        reg = self.chip.get_gpio_chip_select()
        return getattr(reg, 'channel%d_enable'%self.num)

    @cs_enable.setter
    def cs_enable(self, cs_enable):
        reg = registers.one_gpio_chip_select.make(cs_enable)
        self.chip.set_gpio_chip_select(self.num, reg)
