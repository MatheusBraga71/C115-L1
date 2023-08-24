#!/usr/bin/env python

import socket

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = b''
addr = ("djxmmx.net", 17)

s.sendto(message, addr)

data, address = s.recvfrom(1024)
print(data.decode())