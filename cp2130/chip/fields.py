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

import bitstring

from bidict import bidict

from cp2130.chip.base import Field
from cp2130._utils.bcd import *

class BCDField(Field):
    """A 'Field' containing a binary-coded decimal (BCD) integer.

    """

    def to_python(self, value):
        return bcd_to_int(value)

    def from_python(self, value):
        return int_to_bcd(value)

    def default(self):
        return 0

class BytesField(Field):

    def __init__(self, name, length):
        """A 'Field' containing bytes.

        :name: the name of the field
        :length: the number of bytes
        """
        super(BytesField, self).__init__(name, 'bits:%d'%(8*length), b'\x00' * length)

    def to_python(self, value):
        return value.tobytes()

    def from_python(self, value):
        return bitstring.BitArray(bytes = value)

class ConstantField(Field):

    def __init__(self, name, format, value):
        """A 'Field' with a fixed value.

        :name: the name of the field
        :format: the 'bitstring' format for the placeholder
        :value: the constant value
        """
        super(ConstantField, self).__init__(name, '%s'%(format), value)
    
class DictField(Field):

    def __init__(self, name, format, encoding):
        """A 'Field' with the encoding defined by a 'dict'.

        :name: the name of the field
        :format: the 'bitstring' format for the field
        :encoding: a 'dict' mapping the Python values to register values
        """
        super(DictField, self).__init__(name, format, next(iter(encoding)))
        self._encoding = bidict(encoding)

    def to_python(self, value):
        if value not in self._encoding.inv:
            raise ValueError("%s is not a valid value for %s"%(value, self.name))
        return self._encoding.inv[value]

    def from_python(self, value):
        if value not in self._encoding:
            raise ValueError("%s is not a valid value for %s"%(value, self.name))
        return self._encoding[value]

class DiscreteRangeField(Field):

    def __init__(self, name, format, pred, drange):
        """A 'Field' with the encoding representing a discretized range.

        :name: the name of the field
        :format: the 'bitstring' format for the field
        :drange: the discretized range as a list
        :pred: the binary predicate determining if a value matches a
               particular discrete value

        """
        super(DiscreteRangeField, self).__init__(name, format, drange[0])
        self._drange = drange
        self._pred = pred

    def to_python(self, value):
        if value not in range(0, len(self._drange)):
            raise ValueError("%s is not a valid value for %s"%(value, self.name))
        return self._drange[value]

    def from_python(self, value):
        for i in range(len(self._drange)):
            if self._pred(value, self._drange[i]):
                return i
        return i

class IntField(Field):
    """A 'Field' storing an integer.

    """

    def default(self):
        return 0

class BoolField(DictField):
    """A 'Field' for a boolean encoded as a single bit.
    """

    def __init__(self, name):
        super(BoolField, self).__init__(name, 'uint:1', {False: 0, True: 1})
