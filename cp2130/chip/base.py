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
import six
import struct

from enum import Enum

def is_field(value):
    return isinstance(value, Field)

# ================================== Padding ==================================
class Placeholder(object):

    def __init__(self, format):
        """Represents register bits that are not part of a data field.

        :format: the 'bitstring' format for the placeholder

        """
        self.format = format

    def __repr__(self):
        return "Placeholder(%r)"%(self.format)

    def __str__(self):
        return "Placeholder: %s"%(self.format)

def padding(length):
    """Returns a padding placeholder for the specified number of bits.

    :length: the number of bits of padding
    """
    return Placeholder('pad:%d'%length)

# =================================== Field ===================================
class Field(object):

    def __init__(self, name, format, default=None):
        """Represents register bits that form a data field.

        :name: the name of the field
        :format: the 'bitstring' format for the field
        :default: a value used when creating a new register

        """
        self.name        = name
        self.format      = format
        self._default    = default

    def to_python(self, value):
        """Decodes the field value to its Python type.
        """
        return value

    def from_python(self, value):
        """Encodes the Python type to its register value.
        """
        return value

    def default(self):
        return self._default

    def __repr__(self):
        return "Field(%r, %r, default=%r)"%(self.name, self.format, self.default())

    def __str__(self):
        return "%s<%s>"%(self.name, self.format)

# =================================== Register ===================================
class RegisterBase(type):
    """A meta-class that generates properties (setters and getters) for in
    field in the 'pattern' member of the class.

    """

    def __new__(cls, name, bases, attrs):
        # Only generate members and methods on subclasses of Register
        if any(isinstance(b, RegisterBase) for b in bases):
            pattern = attrs['pattern']
            fields  = [f for f in pattern if is_field(f)]

            attrs['_fields'] = fields
            
            # bitstring format 
            attrs['format'] = ", ".join([f.format for f in pattern])

            # properties for each field
            for (idx, f) in enumerate(fields):
                fget = lambda self, i=idx: self._get_field(i)
                fset = lambda self, value, i=idx: self._set_field(i, value)
                attrs[f.name] = property(fget, fset)

            @classmethod
            def make(cls, *values):
                encoded = [f.from_python(v) for (f, v) in zip(cls._fields, values)]
                packed = bitstring.pack(cls.format, *encoded).tobytes()
                return cls(packed)
            attrs['make'] = make

            @classmethod
            def default(cls):
                defaults = [f.default() for f in cls._fields]
                return cls.make(*defaults)
            attrs['default'] = default

        return super(RegisterBase, cls).__new__(cls, name, bases, attrs)

class Register(object, six.with_metaclass(RegisterBase)):

    def __init__(self, raw):
        """A base class for configuration register values.

        The 'pattern' class member list defines the placeholders and
        fields.

        The RegisterBase metaclass generated a 'property' for each
        field.

        """
        if not isinstance(raw, bytes):
            raise ValueError("Argument :raw: must be of type :bytes:")

        self._values = bitstring.BitArray(bytes = raw).unpack(self.format)

        self.name = self.__class__.__name__

    @property
    def raw(self):
        return bitstring.pack(self.format, *self._values).tobytes()

    def _get_field(self, index):
        field = self._fields[index]
        value = self._values[index]
        return field.to_python(value)

    def _set_field(self, index, value):
        field = self._fields[index]
        self._values[index] = field.from_python(value)

    def __repr__(self):
        return "%s(%r)"%(self.name, self.raw)

    def __str__(self):
        pvalues = [f.to_python(v) for (f, v) in zip(self._fields, self._values)]
        
        name_width   = max([len(f.name) for f in self._fields])
        value_width  = max([len('%s'%v) for v in pvalues])
        field_fmt    = "  {0:%d}: {1:%d} ({2})"%(name_width, value_width)

        header = self.name
        fields = [field_fmt.format(f.name, str(pv), str(nv)) for (f, pv, nv) in zip(self._fields, pvalues, self._values)]
        lines  = [header] + fields
        return "\n".join(lines)

# =================================== Commands ===================================
class Dir(Enum):
    IN  = 0
    OUT = 1

class Command(object):

    def __init__(self, direction, bm_request_type, b_request, w_index, w_value, w_length, register_cls, decapitate=False):
        self.direction       = direction
        self.bm_request_type = bm_request_type
        self.b_request       = b_request
        self.w_length        = w_length
        self.w_index         = w_index
        self.register_cls    = register_cls
        self.w_value         = w_value
        self.decapitate      = decapitate

    def to_register(self, data):
        if self.decapitate:
            data = data[1:]
        return self.register_cls(data)

    def to_data(self, register):
        return register.raw

class ArrayCommand(object):

    def __init__(self, direction, bm_request_type, b_request, w_index, w_value, w_length, register_cls, entry_len, entry_offset=-1, decapitate=False):
        self.direction       = direction
        self.bm_request_type = bm_request_type
        self.b_request       = b_request
        self.w_length        = w_length
        self.w_index         = w_index
        self.w_value         = w_value
        self.register_cls    = register_cls
        self.entry_len       = entry_len
        self.entry_offset    = entry_offset
        self.decapitate      = decapitate

    def at(self, offset):
        return ArrayCommand(self.direction, self.bm_request_type, self.b_request, self.w_index, self.w_value, self.w_length, self.register_cls, self.entry_len, offset, self.decapitate)

    def to_register(self, data):
        offset = self.entry_offset * self.entry_len
        entry = data[offset:offset + self.entry_len]
        if self.decapitate:
            entry = entry[1:]
        return self.register_cls(entry)

    def to_data(self, register):
        header = struct.pack('<B', self.entry_offset)
        return header + register.raw

class IndexCommand(object):

    def __init__(self, direction, bm_request_type, b_request, w_value, w_length, register_cls, decapitate=False):
        self.direction       = direction
        self.bm_request_type = bm_request_type
        self.b_request       = b_request
        self.w_length        = w_length
        self.w_value         = w_value
        self.register_cls    = register_cls
        self.decapitate      = decapitate

    def at(self, index):
        return Command(self.direction, self.bm_request_type, self.b_request, index, self.w_value, self.w_length, self.register_cls, self.decapitate)
    
class UnitCommand(object):

    def __init__(self, direction, bm_request_type, b_request, w_index, w_value, w_length):
        self.direction       = direction
        self.bm_request_type = bm_request_type
        self.b_request       = b_request
        self.w_length        = w_length
        self.w_index         = w_index
        self.w_value         = w_value

    def to_data(self, register):
        return b''
