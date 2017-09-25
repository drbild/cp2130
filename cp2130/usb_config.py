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

import codecs

from cp2130.chip import registers
from cp2130.data import Version

class USBConfig(object):
    
    def __init__(self, chip):
        self.chip = chip

    def __repr__(self):
        return "USBConfig(%r)"%(self.chip)

    def __str__(self):
        return """%s:
  Product ID: 0x%x
  Vendor ID: 0x%x
  Manufacturer: %s
  Serial Number: %s
  Release: %s
  Current Required (mA): %s
  Power Mode: %s
  Transfer Priority: %s"""%(self.product_string,
                            self.product_id,
                            self.vendor_id,
                            self.manufacturer_string,
                            self.serial_string,
                            self.release,
                            self.max_power,
                            self.power_mode,
                            self.transfer_priority)

    @property
    def manufacturer_string(self):
        """Get or set the manufacturer string for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        reg1 = self.chip.get_manufacturing_string1()
        reg2 = self.chip.get_manufacturing_string2()
        encoded = (reg1.string + reg2.string)[:reg1.length-2]
        return codecs.decode(encoded, 'utf-16-le')

    @manufacturer_string.setter
    def manufacturer_string(self, string):
        encoded = codecs.encode(string, 'utf-16-le')
        if len(encoded) > 124:
            raise ValueError("Max string length is 62 characters")

        length  = len(encoded) + 2
        encoded = encoded.ljust(124, b'\x00')
        string1 = encoded[:61]
        string2 = encoded[61:]

        reg1 = registers.manufacturing_string1.make(length, 0x03, string1)
        reg2 = registers.manufacturing_string2.make(string2) 

        self.chip.set_manufacturing_string1(reg1)
        self.chip.set_manufacturing_string2(reg2)

    @property
    def product_string(self):
        """Get or set the product string for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        reg1 = self.chip.get_product_string1()
        reg2 = self.chip.get_product_string2()
        encoded = (reg1.string + reg2.string)[:reg1.length-2]
        return codecs.decode(encoded, 'utf-16-le')

    @product_string.setter
    def product_string(self, string):
        encoded = codecs.encode(string, 'utf-16-le')
        if len(encoded) > 124:
            raise ValueError("Max string length is 62 characters")

        length  = len(encoded) + 2
        encoded = encoded.ljust(124, b'\x00')
        string1 = encoded[:61]
        string2 = encoded[61:]

        reg1 = registers.product_string1.make(length, 0x03, string1)
        reg2 = registers.product_string2.make(string2) 

        self.chip.set_product_string1(reg1)
        self.chip.set_product_string2(reg2)

    @property
    def serial_string(self):
        """Get or set the serial string for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        data = self.chip.get_serial_string()
        encoded = data.string[:data.length-2]
        return codecs.decode(encoded, 'utf-16-le')

    @serial_string.setter
    def serial_string(self, string):
        encoded = codecs.encode(string, 'utf-16-le')
        if len(encoded) > 60:
            raise ValueError("Max string length is 30 characters")

        length  = len(encoded) + 2
        string = encoded.ljust(60, b'\x00')

        reg = registers.serial_string.make(length, 0x03, string)
        self.chip.set_serial_string(reg)

    @property
    def vendor_id(self):
        """Get or set the USB vendor id for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        reg = self.chip.get_usb_config()
        return reg.vid

    @vendor_id.setter
    def vendor_id(self, vid):
        reg = registers.usb_config_setter.default()
        reg.vid = vid
        self.chip.set_usb_config(reg)

    @property
    def product_id(self):
        """Get or set the USB product id for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        reg = self.chip.get_usb_config()
        return reg.pid

    @product_id.setter
    def product_id(self, pid):
        reg = registers.usb_config_setter.default()
        reg.pid = pid
        self.chip.set_usb_config(reg)
    
    @property
    def max_power(self):
        """Get or set the required power in milliamps for the device in
        bus-powered mode.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        config = self.chip.get_usb_config()
        return config.max_power_2mA * 2

    @max_power.setter
    def max_power(self, max_power):
        if not (0 <= max_power and max_power <= 500):
            raise ValueError("Max power must between 0 and 500 mA")
        reg = registers.usb_config_setter.default()
        reg.max_power_2mA = int(max_power / 2)
        self.chip.set_usb_config(reg)

    @property
    def power_mode(self):
        """Get or set the power mode for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        reg = self.chip.get_usb_config()
        return reg.power_mode

    @power_mode.setter
    def power_mode(self, power_mode):
        reg = registers.usb_config_setter.default()
        reg.power_mode = power_mode
        self.chip.set_usb_config(reg)

    @property
    def release(self):
        """Get or set the device release (major and minor) number.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        reg = self.chip.get_usb_config()
        return Version(reg.major_release, reg.minor_release)

    @release.setter
    def release(self, release):
        reg = registers.usb_config_setter.default()
        reg.major_release = release.major
        reg.minor_release = release.minor
        self.chip.set_usb_config(reg)

    @property
    def transfer_priority(self):
        """Get or set the data transfer priority for the device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may be changed at once most.

        """
        config = self.chip.get_usb_config()
        return config.transfer_priority

    @transfer_priority.setter
    def transfer_priority(self, transfer_priority):
        reg = registers.usb_config_setter.default()
        reg.transfer_priority = transfer_priority
        self.chip.set_usb_config(reg)
