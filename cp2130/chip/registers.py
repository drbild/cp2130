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

import operator

from cp2130.data import *
from cp2130.data.spi import *
from cp2130.data.event_counter import *
from cp2130.data.gpio import *
from cp2130.chip.base import (
    Field, Register, padding
)
from cp2130.chip.fields import (
    BCDField, BoolField, BytesField, ConstantField, DictField,
    DiscreteRangeField, IntField
)

#===============================================================================
#===================== Configuration and Control Commands ======================
#===============================================================================
class clock_divider(Register):
    pattern = [IntField('clock_divider', 'uint:8')]

class event_counter(Register):
    overflow = BoolField('overflow')
    mode     = DictField('mode', 'uint:3',
                     {EventCounterMode.RISING_EDGE   : 4,
                      EventCounterMode.FALLING_EDGE  : 5,
                      EventCounterMode.NEGATIVE_PULSE: 6,
                      EventCounterMode.POSITIVE_PULSE: 7})
    count    = Field('count', 'uint:8')
    pattern = [overflow, padding(4), mode, count]

class full_threshold(Register):
    threshold = IntField('threshold', 'uint:8')
    pattern = [threshold]

class all_gpio_chip_select(Register):
    def cs(num):
        return BoolField('channel%d_enable'%num)
    pattern = [padding(8), padding(8),
               padding(1), cs(10), cs(9), cs(8), cs(7), cs(6), padding(1), cs(5),
               cs(4), cs(3), cs(2), cs(1), cs(0), padding(3)]

class one_gpio_chip_select(Register):
    control = DictField('control', 'uint:8',
                        {ChipSelectControl.DISABLED          : 0,
                         ChipSelectControl.ENABLED           : 1,
                         ChipSelectControl.ENABLED_EXCLUSIVE : 2})
    pattern = [control]

class all_gpio_mode_and_level(Register):
    def mode_f(num):
        return DictField('gpio%d_mode'%num, 'uint:1',
                         {OutputMode.OPEN_DRAIN: 0,
                          OutputMode.PUSH_PULL : 1})
    def level_f(num):
        return DictField('gpio%d_level'%num, 'uint:1',
                         {LogicLevel.LOW : 0,
                          LogicLevel.HIGH: 1})
    pattern = [level_f(4), level_f(3), level_f(2), level_f(1),
               level_f(0), padding(3),
               padding(1), level_f(10), level_f(9), level_f(8),
               level_f(7), level_f(6), padding(1), level_f(5),
               mode_f(4), mode_f(3), mode_f(2), mode_f(1),
               mode_f(0), padding(3),
               padding(1), mode_f(10), mode_f(9), mode_f(8),
               mode_f(7), mode_f(6), padding(1), mode_f(5)]

    def mode(self, num):
        attr = 'gpio%d_mode'%num
        return getattr(self, attr)

    def level(self, num):
        attr = 'gpio%d_level'%num
        return getattr(self, attr)
    
class one_gpio_mode_and_level(Register):
    mode = DictField('mode', 'uint:8',
                     {GPIOMode.INPUT       : 0x00,
                      OutputMode.OPEN_DRAIN: 0x01,
                      OutputMode.PUSH_PULL : 0x02})
    level = DictField('level', 'uint:8',
                      {LogicLevel.LOW  : 0,
                       LogicLevel.HIGH : 1})
    pattern = [mode, level]

class gpio_values(Register):
    def level_f(num):
        return DictField('gpio%d_level'%num, 'uint:1',
                         {LogicLevel.LOW : 0,
                          LogicLevel.HIGH: 1})
    pattern = [padding(1), level_f(10), level_f(9), level_f(8),
               level_f(7), level_f(6), padding(1), level_f(5),
               level_f(4), level_f(3), level_f(2), level_f(1), level_f(0), padding(3)]

    def level(self, num):
        attr = 'gpio%d_level'%num
        return getattr(self, attr)
    
class rtr_state(Register):
    active = DictField('active', 'uint:8',
                       {False: 0,
                        True : 1})
    pattern = [active]

class spi_word(Register):
    clock_phase      = DictField('clock_phase', 'uint:1',
                                 {ClockPhase.LEADING_EDGE : 0,
                                  ClockPhase.TRAILING_EDGE: 1})
    clock_polarity   = DictField('clock_polarity', 'uint:1',
                                 {ClockPolarity.IDLE_LOW : 0,
                                  ClockPolarity.IDLE_HIGH: 1})
    chip_select_mode = DictField('chip_select_mode', 'uint:1',
                                 {OutputMode.OPEN_DRAIN: 0,
                                  OutputMode.PUSH_PULL: 1})
    clock_frequency  = DiscreteRangeField('clock_frequency', 'uint:3', operator.ge,
                                          [12000000, 
                                           6000000,
                                           3000000,
                                           1500000,
                                           750000,
                                           375000,
                                           187500,
                                           93800])
    pattern = [padding(2), clock_phase, clock_polarity,
               chip_select_mode, clock_frequency]

class spi_delay(Register):
    cs_toggle               = BoolField('cs_toggle')
    pre_deassert            = BoolField('pre_deassert')
    post_assert             = BoolField('post_assert')
    inter_byte              = BoolField('inter_byte')
    inter_byte_delay_10us   = IntField('inter_byte_delay_10us', 'uintbe:16')
    post_assert_delay_10us  = IntField('post_assert_delay_10us', 'uintbe:16')
    pre_deassert_delay_10us = IntField('pre_deassert_delay_10us', 'uintbe:16')
    pattern = [padding(4), cs_toggle, pre_deassert, post_assert, inter_byte,
               inter_byte_delay_10us, post_assert_delay_10us, pre_deassert_delay_10us]

class readonly_version(Register):
    major = IntField('major', 'uint:8')
    minor = IntField('minor', 'uint:8')
    pattern = [major, minor]

#===============================================================================
#======================== OTP ROM Configuration Commands =======================
#===============================================================================
class lock(Register):
    def lock_field(name):
        return DictField(name, 'uint:1',
                         {LockState.LOCKED   : 0,
                          LockState.UNLOCKED : 1})

    transfer_priority     = lock_field('transfer_priority')
    manufacturing_string1 = lock_field('manufacturing_string1')
    manufacturing_string2 = lock_field('manufacturing_string2')
    release_version       = lock_field('release_version')
    power_mode            = lock_field('power_mode')
    max_power             = lock_field('max_power')
    pid                   = lock_field('pid')
    vid                   = lock_field('vid')
    pin_config            = lock_field('pin_config')
    serial_string         = lock_field('serial_string')
    product_string1       = lock_field('product_string1')
    product_string2       = lock_field('product_string2')

    pattern = [transfer_priority, manufacturing_string1, manufacturing_string2,
               release_version, power_mode, max_power, pid, vid,
               padding(4), pin_config, serial_string, product_string2, product_string1]

class manufacturing_string1(Register):
    length          = Field('length', 'uint:8')
    descriptor_type = ConstantField('descriptor_type', 'uint:8', 0x03)
    string          = BytesField('string', 61)
    pattern = [length, descriptor_type, string, padding(8)]

class manufacturing_string2(Register):
    string = BytesField('string', 63)
    pattern = [string, padding(8)]

class pin_config(Register):
    gpio0 = DictField('gpio0', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO0Mode.CS0_n       : 0x03})
    gpio1 = DictField('gpio1', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO1Mode.CS1_n       : 0x03})
    gpio2 = DictField('gpio2', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO2Mode.CS2_n       : 0x03})
    gpio3 = DictField('gpio3', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO3Mode.CS3_n       : 0x03,
                                          GPIO3Mode.RTR_n       : 0x04,
                                          GPIO3Mode.RTR         : 0x05})
    gpio4 = DictField('gpio4', 'uint:8', {GPIOMode.INPUT                         : 0x00,
                                          OutputMode.OPEN_DRAIN                  : 0x01,
                                          OutputMode.PUSH_PULL                   : 0x02,
                                          GPIO4Mode.CS4_n                        : 0x03,
                                          GPIO4Mode.EVENT_COUNTER_RISING_EDGE    : 0x04,
                                          GPIO4Mode.EVENT_COUNTER_FALLING_EDGE   : 0x05,
                                          GPIO4Mode.EVENT_COUNTER_NEGATIVE_PULSE : 0x06,
                                          GPIO4Mode.EVENT_COUNTER_POSITIVE_PULSE : 0x07})
    gpio5 = DictField('gpio5', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO5Mode.CS5_n       : 0x03,
                                          GPIO5Mode.CLKOUT      : 0x04})
    gpio6 = DictField('gpio6', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO6Mode.CS6_n       : 0x03})
    gpio7 = DictField('gpio7', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO7Mode.CS7_n       : 0x03})
    gpio8 = DictField('gpio8', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO8Mode.CS8_n       : 0x03,
                                          GPIO8Mode.SPIACT      : 0x04})
    gpio9 = DictField('gpio9', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                          OutputMode.OPEN_DRAIN : 0x01,
                                          OutputMode.PUSH_PULL  : 0x02,
                                          GPIO9Mode.CS9_n       : 0x03,
                                          GPIO9Mode.SUSPEND     : 0x04})
    gpio10 = DictField('gpio10', 'uint:8', {GPIOMode.INPUT        : 0x00,
                                            OutputMode.OPEN_DRAIN : 0x01,
                                            OutputMode.PUSH_PULL  : 0x02,
                                            GPIO10Mode.CS10_n     : 0x03,
                                            GPIO10Mode.SUSPEND_n  : 0x04})

    def mask_pattern(func):
        return [padding(1),    func('gpio10'), func('gpio9'), func('gpio8'),
                func('gpio7'), func('gpio6'),  func('vpp'),   func('gpio5'),
                func('gpio4'), func('gpio3'),  func('gpio2'), func('gpio1'),
                func('gpio0'), func('mosi'),   func('miso'),  func('sck')]
    
    gpio_pattern = [gpio0, gpio1, gpio2, gpio3, gpio4, gpio5, gpio6, gpio7, gpio8,
                    gpio9, gpio10]

    suspend_level_pattern = mask_pattern(lambda pin: DictField('%s_suspend_level'%pin, 'uint:1',
                                                               {LogicLevel.LOW: 0,
                                                                LogicLevel.HIGH : 1}))

    suspend_mode_pattern  = mask_pattern(lambda pin: DictField('%s_suspend_mode'%pin, 'uint:1',
                                                               {OutputMode.OPEN_DRAIN: 0,
                                                                OutputMode.PUSH_PULL : 1}))

    wakeup_mask_pattern = mask_pattern(lambda pin: BoolField('%s_wakeup_mask'%pin))

    wakeup_match_pattern = mask_pattern(lambda pin: DictField('%s_wakeup_match'%pin, 'uint:1',
                                                              {LogicLevel.LOW: 0,
                                                               LogicLevel.HIGH : 1}))

    divider = [IntField('clock_divider', 'uint:8')]

    pattern = gpio_pattern + suspend_level_pattern + suspend_mode_pattern + wakeup_mask_pattern + wakeup_match_pattern + divider

class product_string1(Register):
    length          = Field('length', 'uint:8')
    descriptor_type = ConstantField('descriptor_type', 'uint:8', 0x03)
    string          = BytesField('string', 61)
    pattern = [length, descriptor_type, string, padding(8)]

class product_string2(Register):
    string = BytesField('string', 63)
    pattern = [string, padding(8)]

class serial_string(Register):
    length          = Field('length', 'uint:8')
    descriptor_type = ConstantField('descriptor_type', 'uint:8', 0x03)
    string          = BytesField('string', 60)
    pattern = [length, descriptor_type, string, padding(8)]

class usb_config(Register):
    vid               = Field('vid', 'uintle:16', default=0)
    pid               = Field('pid', 'uintle:16', default=0)
    max_power_2mA     = Field('max_power_2mA', 'uint:8', default=0)
    power_mode        = DictField('power_mode', 'uint:8',
                                  {PowerMode.BUS_AND_REGULATOR_ON   : 0x00,
                                   PowerMode.SELF_AND_REGULATOR_OFF : 0x01,
                                   PowerMode.SELF_AND_REGULATOR_ON  : 0x02})
    major_release     = BCDField('major_release', 'uint:8')
    minor_release     = BCDField('minor_release', 'uint:8')
    transfer_priority = DictField('transfer_priority', 'uint:8',
                                  {TransferPriority.HIGH_PRIORITY_READ  : 0x00,
                                   TransferPriority.HIGH_PRIORITY_WRITE : 0x01})
    pattern = [vid, pid, max_power_2mA, power_mode,
               major_release, minor_release, transfer_priority]

class usb_config_setter(usb_config):
    write_transfer_priority = BoolField('write_transfer_priority')
    write_release_version   = BoolField('write_release_version')
    write_power_mode        = BoolField('write_power_mode')
    write_max_power_2mA     = BoolField('write_max_power_2mA')
    write_pid               = BoolField('write_pid')
    write_vid               = BoolField('write_vid')
    write_mask_pattern = [write_transfer_priority, padding(2), write_release_version,
                          write_power_mode, write_max_power_2mA, write_pid, write_vid]
    pattern = usb_config.pattern + write_mask_pattern

    def _set_field(self, index, value):
        super(usb_config_setter, self)._set_field(index, value)
        if index == 0:
            self.write_vid = True
        elif index == 1:
            self.write_pid = True
        elif index ==  2:
            self.write_max_power_2mA = True
        elif index == 3:
            self.write_power_mode = True
        elif index == 4:
            self.write_release_version = True
        elif index == 5:
            self.write_release_version = True
        elif index == 6:
            self.write_transfer_priority = True
