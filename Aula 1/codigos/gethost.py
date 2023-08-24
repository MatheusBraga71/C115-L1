import socket
Meu_host_name = socket.gethostname()
print("Nome do host local e {}".format(Meu_host_name))
Meu_IP = socket.gethostbyname(Meu_host_name)
print(" Endereco IP do local host e {}".format(Meu_IP))