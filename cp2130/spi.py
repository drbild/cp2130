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

from cp2130.data.gpio import *
from cp2130.data.spi import *

class SPIChannel(object):

    def __init__(self, master, cs_num):
        """An SPI channel representing a specific slave device attached the
        master.

        :param: master The SPI master device, usually a cp2130.core.CP2130
                       instance.
        :param: cs_num The chip-select number identify the slave
                       device.

        """
        self.master = master
        self.chip   = master.chip
        self.cs_num = cs_num
        self.gpio   = getattr(self.master, 'gpio%d'%cs_num)

        self.gpio.cs_enable = ChipSelectControl.DISABLED

    def __repr__(self):
        return "SPIChannel(%r, %r)"%(self.master, self.cs_num)

    def __str__(self):
        return """SPIChannel.%d
  spi_mode:           %s
  clock_phase:        %s
  clock_polarity:     %s
  cs_mode:            %s
  clock_frequency:    %s
  cs_toggle:          %s
  pre_deassert:       %s
  post_assert:        %s
  inter_byte:         %s
  pre_deassert_delay: %s
  post_assert_delay:  %s
  inter_byte_delay:   %s"""%(self.cs_num,
                             self.spi_mode, self.clock_phase, self.clock_polarity,
                             self.cs_mode, self.clock_frequency, self.cs_toggle,
                             self.pre_deassert, self.post_assert, self.inter_byte,
                             self.pre_deassert_delay, self.post_assert_delay,
                             self.inter_byte_delay)

    def _do(self, op, cs_hold):
        """Assert chip select, perform the given operation, and, if requested,
        deassert the chip-select.

        :param: op The operation to perform.
        :param: cs_hold True if the CS should remain asserted after
                        the read completes. This option is only
                        supported by some implementations.

        """

    def read(self, length, cs_hold = False):
        """Reads the specified number of bytes from the channel.

        :param: cs_hold True if the CS should remain asserted after
                        the read completes. This option is only
                        supported by some implementations.

        """
        op = lambda: self.chip.read(length)
        return self._do(op, cs_hold)

    def write(self, data, cs_hold = False):
        """Writes the specified data from the channel.

        :param: cs_hold True if the CS should remain asserted after
                        the write completes. This option is only
                        support by some implementations.

        """
        op = lambda: self.chip.write(data)
        return self._do(op, data)

    def write_read(self, data, cs_hold = False):
        """Simultaneously writes the specified data to channel and reads the
        same number of bytes.

        :param: cs_hold True if the CS should remain asserted after
                        the operation completes. This option is only
                        support by some implementations.

        """
        op = lambda: self.chip.write_read(data)
        return self._do(op, data)

    @property
    def spi_mode(self):
        """Get or set the SPI mode.

        """
        return SPIMode.of(self.clock_polarity, self.clock_phase)

    @spi_mode.setter
    def spi_mode(self, mode):
        self.clock_polarity = mode.clock_polarity
        self.clock_phase    = mode.clock_phase

    @property
    def clock_phase(self):
        """Get or set the SPI clock phase.

        """
        reg = self.chip.get_spi_word(self.cs_num)
        return reg.clock_phase

    @clock_phase.setter
    def clock_phase(self, clock_phase):
        reg = self.chip.get_spi_word(self.cs_num)
        reg.clock_phase = clock_phase
        self.chip.set_spi_word(self.cs_num, reg)

    @property
    def clock_polarity(self):
        """Get or set the SPI clock phase.
        """
        reg = self.chip.get_spi_word(self.cs_num)
        return reg.clock_polarity

    @clock_polarity.setter
    def clock_polarity(self, clock_polarity):
        reg = self.chip.get_spi_word(self.cs_num)
        reg.clock_polarity = clock_polarity
        self.chip.set_spi_word(self.cs_num, reg)

    @property
    def cs_mode(self):
        """Get or set the chip select mode.

        """
        reg = self.chip.get_spi_word(self.cs_num)
        return reg.chip_select_mode

    @cs_mode.setter
    def cs_mode(self, cs_mode):
        reg = self.chip.get_spi_word(self.cs_num)
        reg.chip_select_mode = cs_mode
        self.chip.set_spi_word(self.cs_num, reg)

    @property
    def clock_frequency(self):
        """Get or set the SPI clock frequency.

        The frequency must be between 93.8 kHz and 12 MHz.

        """
        reg = self.chip.get_spi_word(self.cs_num)
        return reg.clock_frequency

    @clock_frequency.setter
    def clock_frequency(self, clock_frequency):
        reg = self.chip.get_spi_word(self.cs_num)
        reg.clock_frequency = clock_frequency
        self.chip.set_spi_word(self.cs_num, reg)

    @property
    def cs_toggle(self):
        """Get or set the CS toggle enable flag.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        return reg.cs_toggle

    @cs_toggle.setter
    def cs_toggle(self, cs_toggle):
        reg = self.chip.get_spi_delay(self.cs_num)
        reg.cs_toggle = cs_toggle
        self.chip.set_spi_delay(self.cs_num, reg)

    @property
    def pre_deassert(self):
        """Get or set the pre-deassert enable flag.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        return reg.pre_deassert

    @pre_deassert.setter
    def pre_deassert(self, pre_deassert):
        reg = self.chip.get_spi_delay(self.cs_num)
        reg.pre_deassert = pre_deassert
        self.chip.set_spi_delay(self.cs_num, reg)

    @property
    def post_assert(self):
        """Get or set the post-assert delay enable flag.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        return reg.post_assert

    @post_assert.setter
    def post_assert(self, post_assert):
        reg = self.chip.get_spi_delay(self.cs_num)
        reg.post_assert = post_assert
        self.chip.set_spi_delay(self.cs_num, reg)

    @property
    def inter_byte(self):
        """Get or set the inter-byte delay enable flag.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        return reg.inter_byte

    @inter_byte.setter
    def inter_byte(self, inter_byte):
        reg = self.chip.get_spi_delay(self.cs_num)
        reg.inter_byte = inter_byte
        self.chip.set_spi_delay(self.cs_num, reg)

    @property
    def pre_deassert_delay(self):
        """Get or set the pre-deassert delay in microseconds.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        delay = reg.pre_deassert_delay_10us * 10
        return delay

    @pre_deassert_delay.setter
    def pre_deassert_delay(self, pre_deassert_delay):
        reg = self.chip.get_spi_delay(self.cs_num)
        delay = int(pre_deassert_delay / 10)
        reg.pre_deassert_delay_10us = delay
        self.chip.set_spi_delay(self.cs_num, reg)

    @property
    def post_assert_delay(self):
        """Get or set the post-assert delay in microseconds.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        delay = reg.post_assert_delay_10us * 10
        return delay

    @post_assert_delay.setter
    def post_assert_delay(self, post_assert_delay):
        reg = self.chip.get_spi_delay(self.cs_num)
        delay = int(post_assert_delay / 10)
        reg.post_assert_delay_10us = delay
        self.chip.set_spi_delay(self.cs_num, reg)

    @property
    def inter_byte_delay(self):
        """Get or set the inter-byte delay in microseconds.

        """
        reg = self.chip.get_spi_delay(self.cs_num)
        delay = reg.inter_byte_delay_10us * 10
        return delay

    @inter_byte_delay.setter
    def inter_byte_delay(self, inter_byte_delay):
        reg = self.chip.get_spi_delay(self.cs_num)
        delay = int(inter_byte_delay / 10)
        reg.inter_byte_delay_10us = delay
        self.chip.set_spi_delay(self.cs_num, reg)

class SPIChannelCS(SPIChannel):
    """An SPI device addressed using the native chip-select capability of
    the CP2130.

    This class is used for a device connected to a pin configured for
    the CS function.  The CP2130 will automatically assert the CS before an
    SPI transaction and deassert it afterwards.

    """

    def _do(self, op, cs_hold):
        if cs_hold:
            raise NotImplementedError("cs_hold is not supported by the CP2130 native chip-select capability.")
        try:
            self.gpio.cs_enable = ChipSelectControl.ENALBED_EXCLUSIVE
            return op()
        finally:
            self.gpio.cs_enable = ChipSelectControl.DISABLED

class SPIChannelGPIO(SPIChannel):
    """An SPI device addressed using a manually-controlled GPIO on the
    CP2130.

    This class is usd for a device connected to a pin configured as a
    GPIO output.  The class will manually assert the CS before an SPI
    transaction and deassert it afterwards.

    Setting the cs_hold flag of the transfer command will leave the CS
    asserted after the transfer. This is useful if a logic transaction
    is made up of multiple transfers.

    """
    def _do(self, op, cs_hold):
        try:
            self.gpio.value = LogicLevel.LOW
            return op()
        finally:
            if not cs_hold:
                self.gpio.value = LogicLevel.HIGH
