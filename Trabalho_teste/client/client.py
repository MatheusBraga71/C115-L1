# client.py
import socket
import json

# Definindo a porta para a conexão
HOST = "server"
PORT = 12345

# Inicializando o client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtendo o endereço do server (host) por meio do nome
server_ip = socket.gethostbyname(HOST)

# Iniciando a conezão com o servidor
client.connect((server_ip, PORT))
print("Conectado ao servidor.")

for _ in range(3):
    question_data = client.recv(1024).decode()
    pergunta = json.loads(question_data)  # Recebe as perguntas do servidor
    print(pergunta["question"])  # Exibe a pergunta no terminal

    # Exibe as alternativas para a pergunta
    for idx, alternativa in enumerate(pergunta["options"], start=1):
        print(f"{idx}. {alternativa}")

    print("------------------------------")
    # Envia a resposta escolhida para o servidor
    resposta = input("Digite o número da opção com sua resposta: ")
    client.send(resposta.encode())
    print("")

    # Recebe a mensagem de resposta gerada pelo servidor
    mensagem_resposta = client.recv(1024).decode()
    print(mensagem_resposta)

# Recebe a mensagem de resultado final e exibe
result_message = client.recv(1024).decode()
print(result_message)

# Encerra o client
client.close()
