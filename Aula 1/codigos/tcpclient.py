from socket import *   
serverName = 'localhost'
mensagem = "conceitos e tecnologias para dispositivos conectados"
serverPort = 3000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
#a mensagem deve estar em bytes antes de ser enviada ao buffer de transmissao
clientSocket.send(mensagem.encode())
#recebe a resposta do servidor
msg = clientSocket.recv(1024).decode()
#devemos converter a mensagem de volta para string antes de imprimi-la
print('Resposta:' , msg)
#fecha a conexao
clientSocket.close()