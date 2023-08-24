import socket
print("Clinte")
HOST='localhost' 
PORT=57000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("conectando com servidor...")
s.connect((HOST,PORT))
print("abrindo arquivo...")
arq=open('oi.txt','rb')
print("enviado  arquivo")
for i in arq:
    #print i
    s.send(i)
print("saindo...")
arq.close()
s.close()