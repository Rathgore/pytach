#!/usr/bin/env python

import socket
import struct
import sys

def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 9131))

    group = socket.inet_aton('239.255.250.250')
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data = s.recv(1024)
        print('> %s' % data)

def send_command(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('itach.blep.net', 4998))

    s.send(command)
    s.send('\r')

    while True:
        data = s.recv(1024)
        print(data)
        if data.endswith('\r'): break

if __name__ == '__main__':
    send_command(sys.argv[1])
