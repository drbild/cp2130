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

from cp2130.chip.base import (
    ArrayCommand, Command, Dir, IndexCommand, UnitCommand
)

from cp2130.chip.registers import *

#===============================================================================
#===================== Configuration and Control Commands ======================
#===============================================================================
get_clock_divider       =      Command(Dir.IN,  0xC0, 0x46, 0, 0, 0x0001, clock_divider)
get_event_counter       =      Command(Dir.IN,  0xC0, 0x44, 0, 0, 0x0003, event_counter)
get_full_threshold      =      Command(Dir.IN,  0xC0, 0x34, 0, 0, 0x0001, full_threshold)
get_gpio_chip_select    =      Command(Dir.IN,  0xC0, 0x24, 0, 0, 0x0004, all_gpio_chip_select)
get_gpio_mode_and_level =      Command(Dir.IN,  0xC0, 0x22, 0, 0, 0x0004, all_gpio_mode_and_level)
get_gpio_values         =      Command(Dir.IN,  0xC0, 0x20, 0, 0, 0x0002, gpio_values)
get_rtr_state           =      Command(Dir.IN,  0xC0, 0x36, 0, 0, 0x0001, rtr_state)
get_spi_word            = ArrayCommand(Dir.IN,  0xC0, 0x30, 0, 0, 0x000B, spi_word, 1)
get_spi_delay           = IndexCommand(Dir.IN,  0xC0, 0x32,    0, 0x0008, spi_delay, decapitate=True)
get_readonly_version    =      Command(Dir.IN,  0xC0, 0x11, 0, 0, 0x0002, readonly_version)

reset_device            =  UnitCommand(Dir.OUT, 0x40, 0x10, 0, 0, 0)

set_clock_divider       =      Command(Dir.OUT, 0x40, 0x47, 0, 0, 0x0001, clock_divider)
set_event_counter       =      Command(Dir.OUT, 0x40, 0x45, 0, 0, 0x0003, event_counter)
set_full_threshold      =      Command(Dir.OUT, 0x40, 0x35, 0, 0, 0x0001, full_threshold)
set_gpio_chip_select    = ArrayCommand(Dir.OUT, 0x40, 0x25, 0, 0, 0x0002, one_gpio_chip_select, 0)
set_gpio_mode_and_level = ArrayCommand(Dir.OUT, 0x40, 0x23, 0, 0, 0x0003, one_gpio_mode_and_level, 0)
set_gpio_values         =      Command(Dir.OUT, 0x40, 0x21, 0, 0, 0x0004, gpio_values)
#set_rtr_stop            =      Command(Dir.OUT, 0x40, 0x37, 0, 0, 0x0001, rtr_abort)
set_spi_word            = ArrayCommand(Dir.OUT, 0x40, 0x31, 0, 0, 0x0002, spi_word, 1)
set_spi_delay           = ArrayCommand(Dir.OUT, 0x40, 0x33, 0, 0, 0x0008, spi_delay, 1)

#===============================================================================
#======================== OTP ROM Configuration Commands =======================
#===============================================================================
get_lock_byte             =    Command(Dir.IN,  0xC0, 0x6E, 0, 0, 0x0002, lock)
get_manufacturing_string1 =    Command(Dir.IN,  0xC0, 0x62, 0, 0, 0x0040, manufacturing_string1)
get_manufacturing_string2 =    Command(Dir.IN,  0xC0, 0x64, 0, 0, 0x0040, manufacturing_string2)
get_pin_config            =    Command(Dir.IN,  0xC0, 0x6C, 0, 0, 0x0014, pin_config)
get_product_string1       =    Command(Dir.IN,  0xC0, 0x66, 0, 0, 0x0040, product_string1)
get_product_string2       =    Command(Dir.IN,  0xC0, 0x68, 0, 0, 0x0040, product_string2)
get_serial_string         =    Command(Dir.IN,  0xC0, 0x6A, 0, 0, 0x0040, serial_string)
get_usb_config            =    Command(Dir.IN,  0xC0, 0x60, 0, 0, 0x0009, usb_config)

set_lock_byte             =    Command(Dir.OUT, 0x40, 0x6F, 0, 0xA5F1, 0x0002, lock)
set_manufacturing_string1 =    Command(Dir.OUT, 0x40, 0x63, 0, 0xA5F1, 0x0040, manufacturing_string1)
set_manufacturing_string2 =    Command(Dir.OUT, 0x40, 0x65, 0, 0xA5F1, 0x0040, manufacturing_string2)
set_pin_config            =    Command(Dir.OUT, 0x40, 0x6D, 0, 0xA5F1, 0x0014, pin_config)
set_product_string1       =    Command(Dir.OUT, 0x40, 0x67, 0, 0xA5F1, 0x0040, product_string1)
set_product_string2       =    Command(Dir.OUT, 0x40, 0x69, 0, 0xA5F1, 0x0040, product_string2)
set_serial_string         =    Command(Dir.OUT, 0x40, 0x6B, 0, 0xA5F1, 0x0040, serial_string)
set_usb_config            =    Command(Dir.OUT, 0x40, 0x61, 0, 0xA5F1, 0x000A, usb_config_setter)
