# server.py
import socket
import json

# Definindo a porta para a conexão
HOST = "0.0.0.0"
PORT = 12345

# Importando o arquivo JSON com as perguntas
with open("questions.json", "r") as file:
    perguntas = json.load(file)

# Inicializando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print("Servidor aguardando conexões...")

while True:
    client_socket, addr = server.accept()  # Criando a conexão
    print("Cliente conectado:", client_socket.getpeername())
    qtd_acertos = 0  # Variável para armazenar a quantidade de acertos

    for idx, pergunta in enumerate(perguntas, start=1):
        client_socket.send(json.dumps(pergunta).encode())  # Envia uma pergunta para o usuário
        resposta = client_socket.recv(1024).decode()  # Recebe a resposta escolhida pelo usuário
        resposta_usuario = int(resposta)  # Converte o texto da resposta em inteiro para usar como índice depois
        pergunta_acerto = pergunta["correct_answer"]  # Armazena a pergunta em que houve um acerto
        is_correct = resposta_usuario == pergunta_acerto

        if is_correct:  # Se a resposta estiver certa aumenta a contagem de acertos
            qtd_acertos += 1

        escolha_usuario = pergunta["options"][resposta_usuario - 1]  # Armazena a alternativa que o usuário escolheu
        alternativa_correta = pergunta["options"][pergunta_acerto - 1]  # Armazena a alternativa correta da pergunta respondida

        # Gerando a mensagem de resposta
        mensagem_resposta = f"Sua resposta foi: {escolha_usuario}\n"
        if is_correct: mensagem_resposta += "Correto!\n"
        else: mensagem_resposta += f"Incorreto. A resposta correta é: {alternativa_correta}\n"

        # Envia a mensagem de resposta para o client
        client_socket.send(mensagem_resposta.encode())

    # Gera a mensagem de resultado final e envia para o client
    result_message = f"Você acertou {qtd_acertos} de {len(perguntas)} questões."
    client_socket.send(result_message.encode())
client_socket.close()  # Encerra o servidor
