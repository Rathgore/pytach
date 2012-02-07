#!/usr/bin/env python

"""
pytach - A Python module for controlling iTach devices

Copyright (c) 2012 Mark McWilliams (mark@blep.net)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import socket
import struct
import sys
import re

class iTach(object):
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def raw_command(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_address, 4998))

        s.send(command)
        s.send('\r')

        while True:
            data = s.recv(1024)
            if data.endswith('\r'):
                s.close()
                return data.rstrip()

def discover():
    p = re.compile((r'AMXB<-UUID=GlobalCache_(?P<UUID>.{12}).+'
        r'Model=iTach(?P<Model>.+?)>.+'
        r'Revision=(?P<Revision>.+?)>.+'
        r'Config-URL=http://(?P<IP>.+?)>.+'
        r'PCB_PN=(?P<PN>.+?)>.+'
        r'Status=(?P<Status>.+?)>'))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 9131))

    group = socket.inet_aton('239.255.250.250')
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data = s.recv(1024)
        match = p.match(data)
        if match:
            s.close()

            itach = iTach(match.group('IP'))
            itach.uuid = match.group('UUID')
            itach.model = match.group('Model')
            itach.revision = match.group('Revision')
            itach.part_number = match.group('PN')
            itach.status = match.group('Status')
            return itach

if __name__ == '__main__':
    itach = iTach(sys.argv[1])
    print(itach.raw_command(sys.argv[2]))
