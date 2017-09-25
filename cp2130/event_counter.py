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

class EventCounter(object):

    def __init__(self, chip):
        self.chip = chip

    def __repr__(self):
        return "EventCounter(%r)"%(self.chip)

    def __str__(self):
        mode = self.mode
        (count, overflow) = self.count_with_overflow
        return """EventCounter
  mode:     %s
  count:    %s
  overflow: %s"""%(self.mode, count, overflow)

    @property
    def mode(self):
        """Get or set the event count mode.

        Seting the mode will reset the count to zero.

        """
        mode = self.chip.get_event_counter().mode
        return mode

    @mode.setter
    def mode(self, mode):
        reg = registers.event_counter.make(False, mode, 0)
        self.chip.set_event_counter(reg)

    @property
    def count(self):
        """Get or set the event count.

        """
        count = self.chip.get_event_counter().count
        return count

    @count.setter
    def count(self, count):
        reg = self.chip.get_event_counter()
        reg.overflow = False
        reg.count = count
        self.chip.set_event_counter(reg)

    @property
    def count_with_overflow(self):
        """Gets the event count and overflow flag.

        Returns a tuple (count, overflow).

        """
        reg = self.chip.get_event_counter()
        return (reg.count, reg.overflow)
