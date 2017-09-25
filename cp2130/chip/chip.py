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

import six
import struct

from cp2130.chip.commands import *

class ChipBase(type):

    def __new__(cls, cls_name, bases, attrs):
        # Generate a class method for each command
        for name in attrs['commands']:
            cmd    = globals()[name]
            method = {
                Dir.IN : {
                    Command      : lambda self,                  cmd=cmd: self.do_in_command(cmd),
                    ArrayCommand : lambda self, index,           cmd=cmd: self.do_in_command(cmd.at(index)),
                    IndexCommand : lambda self, index,           cmd=cmd: self.do_in_command(cmd.at(index)),
                },
                Dir.OUT: {
                    Command      : lambda self,        register, cmd=cmd: self.do_out_command(cmd, register),
                    ArrayCommand : lambda self, index, register, cmd=cmd: self.do_out_command(cmd.at(index), register),
                    IndexCommand : lambda self, index, register, cmd=cmd: self.do_out_command(cmd.at(index), register),
                    UnitCommand  : lambda self,                  cmd=cmd: self.do_out_command(cmd, None)
                }
            }[cmd.direction][type(cmd)]
            attrs[name] = method
            
        return super(ChipBase, cls).__new__(cls, cls_name, bases, attrs)

class CP2130Chip(object, six.with_metaclass(ChipBase)):

    commands = [
        'get_clock_divider',
        'get_event_counter',
        'get_full_threshold',
        'get_gpio_chip_select',
        'get_gpio_mode_and_level',
        'get_gpio_values',
        'get_rtr_state',
        'get_readonly_version',
        'get_lock_byte',
        'get_manufacturing_string1',
        'get_manufacturing_string2',
        'get_pin_config',
        'get_product_string1',
        'get_product_string2',
        'get_serial_string',
        'get_usb_config',
        'get_spi_word',
        'get_spi_delay',
        'reset_device',
        'set_clock_divider',
        'set_event_counter',
        'set_full_threshold',
        'set_gpio_chip_select',
        'set_gpio_mode_and_level',
        'set_gpio_values',
#        'set_rtr_stop',
        'set_lock_byte',
        'set_manufacturing_string1',
        'set_manufacturing_string2',
        'set_pin_config',
        'set_product_string1',
        'set_product_string2',
        'set_serial_string',
        'set_usb_config',
        'set_spi_word',
        'set_spi_delay'
    ]

    def __init__(self, usb_device):
        self.usb_dev = usb_device

    def do_in_command(self, cmd):
        data = self.usb_dev.control_transfer(cmd.bm_request_type, cmd.b_request, cmd.w_value, cmd.w_index, cmd.w_length)
        return cmd.to_register(data)

    def do_out_command(self, cmd, register):
        data = cmd.to_data(register)
        self.usb_dev.control_transfer(cmd.bm_request_type, cmd.b_request, cmd.w_value, cmd.w_index, data)
        
    def read(self, size):
        command = struct.pack('<HBBI', 0x0000, 0x00, 0x00, size)
        self.usb_dev.write(0x01, command)
        return self.usb_dev.read(0x82, size)

    def write(self, data):
        size = len(data)
        command = struct.pack('<HBBI%ds'%size, 0x0000, 0x01, 0x00, size, data)
        return self.usb_dev.write(0x01, command)

    def write_read(self, data):
        size = len(data)
        command = struct.pack('<HBBI%ds'%size, 0x0000, 0x02, 0x00, size, data)
        self.usb_dev.write(0x01, command)
        return self.usb_dev.read(0x82, size)

    def read_with_rtr(self, size):
        command = struct.pack('<HBBI', 0x0000, 0x04, 0x00, size)
        self.usb_dev.write(0x01, command)
        return self.usb_dev.read(0x82, size)
