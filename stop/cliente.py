import socket
import json

HOST = '127.0.0.1'
PORT = 9000

N_RODADAS = 2
n_rodada_atual = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # enviar nome ao servidor
    nome = input("Nome: ")
    s.sendall(nome.encode())

    while n_rodada_atual <= N_RODADAS:
        # recebe resposta
        resposta = s.recv(1024).decode()

        # enviar respostas
        print(
            f"\nRodada {n_rodada_atual}\n"
            f"{resposta}\n"
            "Envie suas respostas!!"
        )

        # jogador envia suas respostas
        nome = input("nome:")

        # salvar em json
        obj = {
            "nome": nome
        }

        # enviar ao servidor
        obj_str = json.dumps(obj)
        s.sendall(obj_str.encode())

        # pontuacao da rodada
        resposta = s.recv(1024).decode()
        print(f"\n{resposta}")

        n_rodada_atual += 1


    # aguardar classificacao geral
    tabela_classificacao = s.recv(1024).decode()
    print(f"\n{tabela_classificacao}")

