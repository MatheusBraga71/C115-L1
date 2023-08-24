# -*- coding: utf-8 -*-

import random
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12345))

while True:
	
    rand = random.randint(0, 10)

    message, address = serverSocket.recvfrom(1024)
   

    if rand < 4:# taxa de perdas de 40 porcento
        continue

    serverSocket.sendto(message, address)



