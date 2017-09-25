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
from cp2130.data import *
from cp2130.spi import *

from cp2130.clock import Clock
from cp2130.event_counter import EventCounter
from cp2130.gpio import Pin, GPIO
from cp2130.pin_config import PinConfig
from cp2130.usb_config import USBConfig

class CP2130(object):

    def __init__(self, chip):
        """The representation of a CP2130.  This class exposes properties for
        configuring the one-time programmable ROM, setting up the pin
        modes, accessing the clock and event counter features, reading
        and writing the GPIO pins, and obtaining SPI channel instances
        to read and write to SPI slaves.

        :param: chip The underlying cp2130.chip.CP2130Chip instance.

        """
        self.chip = chip

        self.clock         = Clock(chip)
        self.event_counter = EventCounter(chip)

        self.usb = USBConfig(chip)
        
        self.miso   = Pin('miso', chip)
        self.mosi   = Pin('mosi', chip)
        self.sck    = Pin('sck', chip)
        self.vpp    = Pin('vpp', chip)
        
        self.gpio0  = GPIO( 0, chip)
        self.gpio1  = GPIO( 1, chip)
        self.gpio2  = GPIO( 2, chip)
        self.gpio3  = GPIO( 3, chip)
        self.gpio4  = GPIO( 4, chip)
        self.gpio5  = GPIO( 5, chip)
        self.gpio6  = GPIO( 6, chip)
        self.gpio7  = GPIO( 7, chip)
        self.gpio8  = GPIO( 8, chip)
        self.gpio9  = GPIO( 9, chip)
        self.gpio10 = GPIO(10, chip)

        def channel_for(gpio):
            function = gpio.function
            if function in [OutputMode.PUSH_PULL, OutputMode.OPEN_DRAIN]:
                return SPIChannelGPIO(self, gpio.num)
            else:
                return SPIChannelCS(self, gpio.num)
        
        self.channel0  = channel_for(self.gpio0)
        self.channel1  = channel_for(self.gpio1)
        self.channel2  = channel_for(self.gpio2)
        self.channel3  = channel_for(self.gpio3)
        self.channel4  = channel_for(self.gpio4)
        self.channel5  = channel_for(self.gpio5)
        self.channel6  = channel_for(self.gpio6)
        self.channel7  = channel_for(self.gpio7)
        self.channel8  = channel_for(self.gpio8)
        self.channel9  = channel_for(self.gpio9)
        self.channel10 = channel_for(self.gpio10)

    @property
    def full_threshold(self):
        """Get or set the FIFO full threshold in bytes.

        The threshold must be between 1 and 255.

        """
        threshold = self.chip.get_full_threshold().threshold
        return threshold

    @full_threshold.setter
    def full_threshold(self, threshold):
        if not (1 <= threshold and threshold <= 255):
            raise ValueError("Threshold must be between 1 and 255 bytes")
        reg = registers.full_threshold.make(threshold)
        self.chip.set_full_threshold(reg)

    @property
    def version(self):
        """Get the read-only version of the chip.

        """
        version = self.chip.get_readonly_version()
        return Version(version.major, version.minor)

    def reset(self):
        """Resets the device.  After approximately one millisecond, the device
        will reset and reenumerate on the USB bus.

        """
        self.chip.reset_device()
        
    @property
    def lock(self):
        """Get or set the one-time programmable lock byte, which indicates the
        fields that may not be programmed.

        Locked fields cannot be unlocked.  Each field may be
        explicitly lock using this property. Fields are implicitly
        locked when modified.

        """
        lock = self.chip.get_lock_byte()
        return lock

    @lock.setter
    def lock(self, lock):
        self.chip.set_lock_byte(lock)

    @property
    def pin_config(self):
        """Get or set the initial pin configuration for this device.

        WARNING: This field is stored in the one-time programmable
        ROM. It may changed at once most.

        """
        reg = self.chip.get_pin_config()
        return PinConfig(reg)

    @pin_config.setter
    def pin_config(self, pin_config):
        self.chip.set_pin_config(pin_config.register)
