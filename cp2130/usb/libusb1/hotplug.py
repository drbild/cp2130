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

import logging
import threading
import usb1

import cp2130.usb.usb

class HotpluggedDevice(object):

    def __init__(self, device):
        """A USB device that can call a given function when then physical
        device is unplugged.

        """
        self.device = device
        self._listener = None
        self._unplugged_callback = None

    def close(self):
        self._stop()

    @property
    def bus(self):
        return self.device.getBusNumber()

    @property
    def address(self):
        return self.device.getDeviceAddress()

    @property
    def pid(self):
        return self.device.getProductID()

    @property
    def vid(self):
        return self.device.getVendorID()

    def _start(self):
        if self._listener == None:
            self._listener = HotplugListener(self.vid, self.pid, None, self._on_left_event)
            self._listener.start()

    def _stop(self):
        if self._listener != None:
            self._listener.stop()
            self._listener = None

    def register_unplugged_callback(self, callback):
        """Registers a callback to be invoked when the device is unplugged.

        :param: callback The zero-argument function to invoke.

        """
        self._unplugged_callback = callback
        self._start()

    def unregister_unplugged_callback(self):
        """Unregisters the callback, if one was registered.

        """
        self._stop()
        self._unplugged_callback = None

    def is_same_device(self, device):
        bus     = device.getBusNumber()
        address = device.getDeviceAddress()
        return bus == self.bus and address == self.address

    def _on_left_event(self, device):
        if self.is_same_device(device):
            if self._unplugged_callback:
                self._unplugged_callback()

class HotplugListener(cp2130.usb.usb.HotplugListener):

    def __init__(self, vid, pid, on_arrived_event=None, on_left_event=None):
        """A listener for hotplug 'arrived' and 'left' events on devices
        matching the specified vendor id and product id.

        """
        self._vid = vid
        self._pid = pid
        self._on_arrived_event = on_arrived_event
        self._on_left_event = on_left_event

        self._running = False
        self._thread = None

    def _verify_hotplug_support(self):
        with usb1.USBContext() as context:
            if not context.hasCapability(usb1.CAP_HAS_HOTPLUG):
                raise NoHotplugSupportError("Hotplug support is missing. Please update your libusb version.")

    def start(self):
        self._verify_hotplug_support()
        self._running = True
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        if self._running:
            self._running = False

    def _loop(self):
        with usb1.USBContext() as context:
            h = context.hotplugRegisterCallback(self._on_event,
                                                events = usb1.HOTPLUG_EVENT_DEVICE_ARRIVED | \
                                                         usb1.HOTPLUG_EVENT_DEVICE_LEFT,
                                                vendor_id  = self._vid,
                                                product_id = self._pid)
            try:
                while self._running:
                    context.handleEventsTimeout(0.1)
            finally:
                context.hotplugDeregisterCallback(h)

    def _on_event(self, context, device, event):
        if event == usb1.HOTPLUG_EVENT_DEVICE_ARRIVED:
            cb = self._on_arrived_event
        elif  event == usb1.HOTPLUG_EVENT_DEVICE_LEFT:
            cb = self._on_left_event

        if cb:
            try:
                cb(device)
            except Exception as e:
                log = logging.getLogger("cp2130.usb.libusb1")
                log.error("Error in callback for hotplug event", exc_info=True)
