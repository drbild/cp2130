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

def bcd_to_int(bcd):
    """Converts a 1-byte binary-coded decimal to an integer.

    :param bcd: the 1-byte binary-coded decimal as a Python `int`.
    :returns: the integer value as a Python `int`.
    """
    assert(0 <= bcd and bcd <= 255)
    ones = bcd & 0b1111
    tens = bcd >> 4
    return 10*tens + ones

def int_to_bcd(integer):
    """Converts a two-digit, non-negative integer (0-99) to a one-byte
    binary coded decimal.

    :param: the integer value as a Python `int`.
    :returns: the 1-byte binary-coded decimal as a Python `int`.
    """
    assert(0 <= integer and integer <= 99)
    ones = integer % 10
    tens = integer // 10
    return (tens << 4) | ones
