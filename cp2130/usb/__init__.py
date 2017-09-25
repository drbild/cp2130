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

def find(vid=0x10c4, pid=0x87A0):
    """Finds the first USB device with the given vendor id and product
    id.

    Uses the PyUSB library internally to query the USB bus.

    :param: vid The vendor id to match.
    :param: pid The product id to match.
    :return: A USBDevice instance wrapping the matched device.
    :raises: A NoDeviceError error if no matching device is found.

    """
    import cp2130.usb.pyusb
    dev = pyusb.find(idVendor, idProduct)
    return core.CP2130(dev)
