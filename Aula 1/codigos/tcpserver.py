from socket import *  

serverPort = 3000
serverSocket = socket(AF_INET, SOCK_STREAM)
#atribui a porta ao socket criado
serverSocket.bind(('', serverPort))    
#aceita conexoes 
#com no maximo um cliente na fila 
serverSocket.listen(1)
print('The server is ready to receive')
while True:
	connectionSocket, addr = serverSocket.accept()         
	#recebe a mensagem do cliente em bytes
	mensagem = connectionSocket.recv(1024)     
	#envio tbm deve ser em bytes
	mensagem = mensagem.upper()
	connectionSocket.send(mensagem)
	connectionSocket.close()