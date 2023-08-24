import socket
print("Servidor")
HOST = "localhost" 
PORT = 57000
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Escutando a porta...")
s.bind((HOST,PORT))
s.listen(1)
print("Aceitando a conexao...")
conn,addr= s.accept()
print("recebendo o arquivo...")
arq = open('oi.txt','wb')
while 1:
 
    dados=conn.recv(1024)
    if not dados:
        break
    arq.write(dados)
print("saindo...")
arq.close()
conn.close()