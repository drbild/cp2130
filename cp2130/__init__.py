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

from cp2130.core import CP2130
from cp2130.data import *

def find(vid=0x10c4, pid=0x87A0):
    """Find the first CP2130 with the given vendor id and product id.

    :param: vid The vendor id to match.
    :param: pid The product id to match.
    :return: A cp2130.core.CP2130 instance for the matched device.
    :raises: A cp2130.usb.NoDeviceError if no matching device is found.
    """
    from cp2130.chip import CP2130Chip
    from cp2130.core import CP2130

    try:
        from cp2130.usb import libusb1 as usb
    except:
        raise
        from cp2130.usb import pyusb as usb
    
    dev  = usb.find(vid, pid)
    chip = CP2130Chip(dev)
    return CP2130(chip)

def hotplug(on_plugged, vid=0x10c4, pid=0x87A0):
    """Register a function to call with each hotplugged CP2130 matching
    the given vendor id and product id.

    :param: on_plugged A one-argument function to invoke with a
                       cp1230.core.CP2130 instance for each matching
                       hotplugged device.
    :param: vid The vendor id to match.
    :param: pid The product id to match.

    :return: A cp2130.usb.HotplugListener instance. Call '#stop()' to
    stop receiving events.

    """
    from cp2130.chip import CP2130Chip
    from cp2130.core import CP2130

    try:
        from cp2130.usb import libusb1 as usb
    except:
        import logging
        logging.getLogger().error("asdf", exc_info=True)
        from cp2130.usb import pyusb as usb

    def on_new_device(dev):
        chip = CP2130Chip(dev)
        on_plugged(CP2130(chip))

    return usb.hotplug(vid, pid, on_new_device)
