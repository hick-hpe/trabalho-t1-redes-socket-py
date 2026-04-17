"""
Antes de enviar mensagens, o cliente deve enviar seu nome ao servidor. Este nome será mostrado nas mensagens;
"""

import socket

HOST = "127.0.0.1"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    print("\n--------- Bem vindo ao ChatServer ---------\n")

    print('Para entrar, insira seu nome')
    nome = input(": ")
    cliente.sendall(f"/nome {nome}".encode())

    # apos receber confirmacao de registro, pode comecar a enviar as mensagens
    resposta_login = cliente.recv(1024).decode() # OK

    try:
        # permitir o envio de mensagens
        print('\n--------- Agora pode enviar mensagens!! ---------\n')
        while True:
            mensagem = input(": ")
            cliente.sendall(mensagem.encode())
    
    except KeyboardInterrupt:
        print("You left the game")
    
    

