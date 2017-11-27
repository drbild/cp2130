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

import usb

def find(vid, pid):
    """Finds the first USB device with the given vendor id and product id.

    :param: vid The vendor id to match.
    :param: pid The product id to match.
    :return: A PyUSBDevice instance wrapping the matched device.
    :raises: A NoDeviceError error if no matching device is found.
    """
    dev = usb.core.find(idVendor=vid, idProduct=pid)
    if dev is None:
        raise NoDeviceError("No device with vendor %s and product %s"%(vid, pid))

    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)

    dev.get_active_configuration()

    return PyUSBDevice(dev)

class PyUSBDevice(USBDevice):

    def __init__(self, device):
        """An abstraction of a USB device accessed via the PyUSB library.

        """
        self.device = device

    def endpoints(self):
        """Gets all the endpoint addresses supported by the underlying device.

        """
        config = self.device.get_active_configuration()
        interface = config.interfaces()[0]
        endpoints = interface.endpoints()
        return [endpoint.bEndpointAddress for endpoint in endpoints]

    def control_transfer(self, bmRequestType, bRequest, wValue, wIndex, wLengthOrData):
        """Issues a control request to the underlying device.

        """
        response = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLengthOrData)
        try:
            return response.tostring()
        except:
            return response

    def read(self, endpoint, size):
        """Reads the requested number of bytes from the specified endpoint.

        """
        return self.device.read(endpoint, size)

    def write(self, endpoint, data):
        """Writes the given data to the specified endpoint.

        """
        return self.device.write(endpoint, data)
