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

from setuptools import setup, Extension

import sys

setup(
    name = 'cp2130',
    version = '1.0.2',
    description = 'Library for the Silicon Labs CP2130 USB to SPI Bridge',
    author = 'David R. Bild',
    author_email = 'david@davidbild.org',
    license="Apache 2.0",
    url = 'https://github.com/drbild/cp2130',
    download_url = 'https://github.com/drbild/cp2130/archive/1.0.2.tar.gz',
    keywords = ['usb', 'spi', 'bridge', 'Silicon Labs', 'silabs', 'cp2130', 'cp213x'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft'
    ],
    packages = ['cp2130',
                'cp2130.chip',
                'cp2130.data',
                'cp2130.usb',
                'cp2130._utils'],
    install_requires = ['bidict', 'bitstring', 'enum34', 'pyusb', 'six'],
    zip_safe = False
)
