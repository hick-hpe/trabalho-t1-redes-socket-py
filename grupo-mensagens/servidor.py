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
def acessar_mensagem_recente(conn):

    print("Tentando ler mensagens...")

    # aguarda até que existam mensagens
    SEMAFORO_MENSAGENS.acquire()

    # aguarda o acesso
    SEMAFORO_ACESSO.acquire()

    # Verifica se há mensagens na fila
    if mensagens:
        # obtem a primeira mensagem da fila
        mensagem = mensagens.pop(0)

    # libera o acesso
    SEMAFORO_ACESSO.release()

    # envia as mensagens ao container de mensagens
    resposta = json.dumps(mensagem)
    conn.sendall(resposta.encode())


# metodo para formatar a saida da mensagem
def formatar_mensagem(conn, mensagem):
    nome = usuarios[conn]["nome"]
    IP = usuarios[conn]["IP"]
    data_mensagem = datetime.now()

    formatada = f"[{nome} ({IP}) {data_mensagem.strftime('%H:%M:%S')}]"
    formatada += f"\n{mensagem}"

    return formatada


# metodo para registrar usuario
def registrar_usuario(conn, addr, data):
    nome = data.decode().split()

    print("Registrado...")

    # obtem o nome
    nome = data.decode()

    # registra o usuario
    usuarios[conn] = {
        "nome": nome,
        "IP": addr[0]
    }
    conn.sendall(b"OK")
    

# metodo para receber e salvar a mensagem
def salvar_mensagem(conn, data):
    print("Tentando enviar mensagens...")

    # obtem a mensagem
    mensagem = data.decode()

    print('/msg:', mensagem)

    # solicitar o acesso
    SEMAFORO_ACESSO.acquire()

    # salvar a mensagem
    mensagens.append(formatar_mensagem(conn, mensagem))

    # libera o acesso as mensagens
    SEMAFORO_ACESSO.release()

    # avisar quando chegar mensagens
    SEMAFORO_MENSAGENS.release()


# metodo da thread para receber os dados enviados pelos clientes
def receber_dados_socket(conn,addr):

    while True:
        # recebe o dado
        data = conn.recv(1024)

        # se o cliente nao enviou dados, desconectado 
        if not data:
            print("Cliente desconectou.")
            break
        
        # diferenciar as threads de listagem e de receber mensagens
        if data.decode() == "/listar":
            acessar_mensagem_recente(conn)
        
        elif data.decode().startswith("/nome"):
            registrar_usuario(conn, addr, data)

        else:
            salvar_mensagem(conn, data)

        
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
        thread = threading.Thread(target=receber_dados_socket, args=(conn,addr,))
        thread.start()
