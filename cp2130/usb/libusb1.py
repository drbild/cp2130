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

from cp2130.usb.usb import NoDeviceError, USBDevice

import array
import usb1

def find(vid, pid):
    """Finds the first USB device with the given vendor id and product id.

    :param: vid The vendor id to match.
    :param: pid The product id to match.
    :return: A LibUSB1Device instance wrapping the matched device.
    :raises: A NoDeviceError error if no matching device is found.
    """
    context = usb1.USBContext()

    handle = context.openByVendorIDAndProductID(vid, pid, skip_on_error = True)
    if handle is None:
        raise NoDeviceError("No device with vendor %s and product %s"%(vid, pid))

    if handle.kernelDriverActive(0):
        handle.detachKernelDriver(0)

    return LibUSB1Device(context, handle)

class LibUSB1Device(USBDevice):

    def __init__(self, context, handle):
        """An abstraction of a USB device accessed via the libusb1 library.

        """
        self.context = context
        self.handle = handle
        self.handle.claimInterface(0)

    def close(self):
        self.handle.releaseInterface(0)
        self.handle.close()
        self.handle = None

        self.context.close()
        self.context = None

    def endpoints(self):
        """Gets all the endpoint addresses supported by the underlying device.

        """
        device    = self.handle.getDevice()
        config    = next(device.iterConfigurations())
        interface = next(config.iterInterfaces())
        settings  = next(interface.iterSettings())
        endpoints = settings.iterEndpoints()
        return [endpoint.getAddress() for endpoint in endpoints]

    def control_transfer(self, bmRequestType, bRequest, wValue, wIndex, wLengthOrData):
        """Issues a control request to the underlying device.

        """
        if type(wLengthOrData) == int:
            return bytes(self.handle.controlRead(bmRequestType, bRequest, wValue, wIndex, wLengthOrData))
        else:
            return self.handle.controlWrite(bmRequestType, bRequest, wValue, wIndex, wLengthOrData)

    def read(self, endpoint, size):
        """Reads the requested number of bytes from the specified endpoint.

        """
        return array.array('B', self.handle.bulkRead(endpoint, size))

    def write(self, endpoint, data):
        """Writes the given data to the specified endpoint.

        """
        return self.handle.bulkWrite(endpoint, data)
