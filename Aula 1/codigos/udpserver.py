from socket import *
#Porta do servidor
PortaServidor= 12000

SocketServidor = socket(AF_INET,SOCK_DGRAM)
SocketServidor.bind(('',PortaServidor))
SocketServidor.settimeout(1000)

print("Server Ready")
while 1:

	Palavra,EnderecoCliente = SocketServidor.recvfrom(1024)
	PalavraModificada =Palavra.decode('utf-8').upper()
	print("Enviando para o cliente: ",PalavraModificada)
	SocketServidor.sendto(PalavraModificada.encode('utf-8'),EnderecoCliente)