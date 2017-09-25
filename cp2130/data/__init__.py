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

from cp2130.data.event_counter import *
from cp2130.data.gpio import *
from cp2130.data.rom import *
from cp2130.data.spi import *
from cp2130.data.usb import *

class Version(object):

    def __init__(self, major, minor):
        """A version number comprising a major and minor number.

        """
        self.major = major
        self.minor = minor

    def __repr__(self):
        return "Version(%d, %d)"%(self.major, self.minor)

    def __str__(self):
        return "%d.%d"%(self.major, self.minor)
