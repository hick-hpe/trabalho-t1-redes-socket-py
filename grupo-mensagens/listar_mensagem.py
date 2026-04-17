"""
As mensagens apresentadas devem conter nome e IP do cliente e o horário em que o servidor recebeu a mensagem;

O acesso à fila de mensagens no servidor deve ser protegido contra acesso concorrente, utilizando semáforos.
"""

import socket
import json

HOST = "127.0.0.1"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    print("\n--------- ChatServer ---------\n")
    
    while True:
        # solicitar mensagens
        cliente.sendall(b"/listar")

        # aguarda o envio dos dados
        data = cliente.recv(1024)

        # recebe as mensagens do chat
        mensagem = json.loads(data.decode())

        # exibir mensagem
        print(f"{mensagem}\n")


