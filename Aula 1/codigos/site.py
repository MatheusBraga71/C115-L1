import socket
from pprint import pprint


addrinfo = socket.getaddrinfo('uol.com.br', 'www')

pprint(addrinfo)


