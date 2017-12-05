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

from cp2130.usb.usb import NoDeviceError, NoHotplugSupportError, USBDevice
from cp2130.usb.libusb1.hotplug import HotplugListener, HotpluggedDevice

import array
import usb1

def hotplug(vid, pid, on_new_device):
    def create_device(device):
        dev = find_exact(device.getBusNumber(), device.getDeviceAddress())
        if dev:
            on_new_device(dev)

    listener = HotplugListener(vid, pid, create_device, None)
    listener.start()
    return listener

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

    return LibUSB1Device(context, handle)

def find_exact(bus, address):
    """Finds the USB device on the given bus at the given address.

    :param: bus The bus the device is on.
    :param: address The address of the device on the bus.
    :return: A LibUSB1Device instance wrapping the matched device.
    :raises: A NoDeviceError error if no matching device is found.
    """
    context = usb1.USBContext()

    for d in context.getDeviceList(skip_on_error=True):
        if d.getBusNumber() == bus and d.getDeviceAddress() == address:
            handle = d.open()
            return LibUSB1Device(context, handle)

    raise NoDeviceError("No device with bus %d and address %d"%(bus, address))

class LibUSB1Device(USBDevice, HotpluggedDevice):

    def __init__(self, context, handle):
        """An abstraction of a USB device accessed via the libusb1 library.

        """
        HotpluggedDevice.__init__(self, handle.getDevice())

        self.timeout = 1000
        self.context = context
        self.handle = handle

        if self.handle.kernelDriverActive(0):
            self.handle.detachKernelDriver(0)

        self.handle.claimInterface(0)

    def close(self):
        HotpluggedDevice.close(self)

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
            return array.array('B', self.handle.controlRead(bmRequestType, bRequest, wValue, wIndex, wLengthOrData, timeout=self.timeout))
        else:
            return self.handle.controlWrite(bmRequestType, bRequest, wValue, wIndex, wLengthOrData, timeout=self.timeout)

    def read(self, endpoint, size):
        """Reads the requested number of bytes from the specified endpoint.

        """
        return array.array('B', self.handle.bulkRead(endpoint, size, timeout=self.timeout))

    def write(self, endpoint, data):
        """Writes the given data to the specified endpoint.

        """
        return self.handle.bulkWrite(endpoint, data, timeout=self.timeout)
