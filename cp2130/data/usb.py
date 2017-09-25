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

from enum import Enum

class TransferPriority(Enum):
    """USB transfer priority.

    """
    HIGH_PRIORITY_READ  = 0
    HIGH_PRIORITY_WRITE = 1

class PowerMode(Enum):
    """CP2130 power mode.

    """
    BUS_AND_REGULATOR_ON   = 0
    SELF_AND_REGULATOR_OFF = 1
    SELF_AND_REGULATOR_ON  = 2
