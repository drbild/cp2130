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

class NoDeviceError(EnvironmentError):
    """An error raised if no USB device matching the specified criteria is
    found.

    """
    pass

class USBDevice(object):
    """An abstraction of a USB device. Implementations of the interface
    will use a specific library to access the actual CP2130 USB device
    on the host computer.

    A default implemention wrapping the PyUSB library is provided in
    the cp2130.usb.pyusb module.

    """

    def endpoints(self):
        """Gets all the endpoint addresses supported by the underlying device.

        """
        raise NotImplementedError

    def control_transfer(self, bmRequestType, bRequest, wValue, wIndex, wLengthOrData):
        """Issues a control transfer request to the underlying device.

        """
        raise NotImplementedError

    def read(self, endpoint, size):
        """Reads the requested number of bytes from the specified endpoint.

        """
        raise NotImplementedError

    def write(self, endpoint, data):
        """Writes the given data to the specified endpoint.

        """
        raise NotImplementedError
