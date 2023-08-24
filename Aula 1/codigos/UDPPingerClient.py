import time
from socket import *

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
remoteAddr = (gethostname(), 12345)
for i in range(10):
    
    sendTime = time.time()
    message = 'PING ' + str(i + 1) + " " + str(time.strftime("%H:%M:%S"))
    clientSocket.sendto(message.encode(), remoteAddr)

    try:
        data, server = clientSocket.recvfrom(1024)
        Data=data.decode()
        recdTime = time.time()
        rtt = recdTime - sendTime
        print("Message Received", Data)
        print("Round Trip Time", rtt)
        print()

    except timeout:
        print('REQUEST TIMED OUT')
        print()
clientSocket.close()