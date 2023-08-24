from socket import *  
#Server Addess.  
servername = 'localhost'  
serverPort = 12000  
#Create an INET , STREAM socket (UDP).  
clientSocket = socket(AF_INET,SOCK_DGRAM)  
clientSocket.connect((servername,serverPort))  
clientSocket.settimeout(10)  
sentence = input('Input text: ')  
#sendto server adress + server port. 
clientSocket.sendto(sentence.encode('utf-8'),(servername,serverPort))  
modifiedSentence= clientSocket.recv(1024)  
print("From server: ",modifiedSentence.decode('utf-8'))  
clientSocket.close() 