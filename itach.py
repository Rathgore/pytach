#!/usr/bin/env python

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
            if data.endswith('\r'): return data

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
