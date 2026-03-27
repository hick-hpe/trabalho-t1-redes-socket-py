"""
O servidor deve suportar múltiplos clientes simultâneamente, utilizando threads;
"""

import threading
import socket
from datetime import datetime
import json

HOST = "0.0.0.0"
PORT = 9000
usuarios = {}
mensagens = []

# semaforos
SEMAFORO_ACESSO = threading.Semaphore(1)
SEMAFORO_MENSAGENS = threading.Semaphore(0)

# metodo para obter as mensagens do chat
def acessar_mensagem_recente(conn, data):

    print("Tentando ler mensagens...")

    # aguarda até que existam mensagens
    SEMAFORO_MENSAGENS.acquire()

    # aguarda o acesso
    SEMAFORO_ACESSO.acquire()

    # Verifica se há mensagens na fila
    if mensagens:
        # obtem a primeira mensagem da fila
        mensagem = mensagens[0]

    # libera o acesso
    SEMAFORO_ACESSO.release()

    # envia as mensagens ao container de mensagens
    resosta = json.dumps(mensagens[-1])
    conn.sendall(resosta.encode())


# metodo para formatar a saida da mensagem
def formatar_mensagem(conn, mensagem):
    nome = usuarios[conn]["nome"]
    IP = usuarios[conn]["IP"]
    data_mensagem = datetime.now()

    formatada = f"[{nome} ({IP}) {data_mensagem.strftime('%I:%M %p')}]"
    formatada += f"\n{mensagem}"

    return formatada


# metodo para receber e salvar a mensagem
def receber_e_salvar_mensagem(conn, data):
    print("Tentando enviar mensagens...")

    # verifica se o usuario ja registrado
    if conn not in usuarios:
        print("Registrado...")

        # obtem o nome
        nome = data.decode()

        # registra o usuario
        usuarios[conn] = {
            "nome": nome,
            "IP": addr[0]
        }

        conn.sendall(b"OK")
    
    else:
        # obtem a mensagem
        mensagem = data.decode()

        # solicitar o acesso
        SEMAFORO_ACESSO.acquire()

        # salvar a mensagem
        mensagens.append(formatar_mensagem(conn, mensagem))

        # libera o acesso as mensagens
        SEMAFORO_ACESSO.release()

        # avisar quando chegar mensagens
        SEMAFORO_MENSAGENS.release()


# metodo da thread para receber os dados enviados pelos clientes
def receber_dados_socket(conn):

    while True:
        # recebe o dado
        data = conn.recv(1024)

        # se o cliente nao enviou dados, desconectado 
        if not data:
            print("Cliente desconectou.")
            break
        
        # diferenciar as threads de listagem e de receber mensagens
        if data.decode() == "/listar":
            acessar_mensagem_recente(conn, data)
        else:
            receber_e_salvar_mensagem(conn, data)

        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    s.settimeout(500)

    print('\n--- Iniciando ChatServer ---\n')

    # recebe a conexao do cliente
    while True:
        # recebe conexao do cliente
        conn, addr = s.accept()

        # cria a thread responsavel por ler os dados do socket
        thread = threading.Thread(target=receber_dados_socket, args=(conn,))
        thread.start()
