import json
import socket
import threading
from random import randint
import time

HOST = '0.0.0.0'
PORT = 9000

# dados do jogo
NUM_JOGADORES = 3
N_RODADAS = 2
WAITING_TIME = 2
jogadores = {}


# calcula a pontuacao dos jogadores
def calcular_pontuacao():
    # lista de temas
    temas = [
        "nome"
    ]

    # organizar as respostas recebidas por temas
    respostas = {t: {} for t in temas}

    # organizar as respostas iguais
    i = 1
    for conn in jogadores:
        # jogador
        jog = jogadores[conn]

        # respostas do jogador (jog["resp"]) por tema
        for tema in jog["resp"]:

            # se a resposta nao esta na lista geral, adicionar a chave do jogador
            resposta = jog["resp"][tema]
            if resposta not in respostas[tema]:
                respostas[tema][resposta] = [conn]
            else:
                respostas[tema][resposta].append(conn)

        i += 1
    

    # contar os pontos
    for tema in respostas:
        for resposta in respostas[tema]:
            lista_jog = respostas[tema][resposta]
            # print(f'[{tema}] responderam "{resposta}": {list(jogadores[conn]["nome"] for conn in lista_jog)}')
    
            # se mais de um jogador respondeu a mesma coisa, todos ganham 1 ponto
            if len(lista_jog) > 1:
                for conn in lista_jog:
                    jogadores[conn]["pontos"] += 1
            
            # se foi o unico a responder isso, ganha 3 pontos
            else:
                conn = lista_jog.pop()
                jogadores[conn]["pontos"] += 3


# salvar as respostas do jogador
def salvar_respostas_jogador(conn):
    resposta = conn.recv(1024).decode()
    obj_resp = json.loads(resposta)
    jogadores[conn]["resp"] = obj_resp


def criar_tabela_classificacao():
    tabela_classificacao = f"{'Nome'.ljust(10)} | {'Pontuação'.ljust(2)}\n"
    largura = len(tabela_classificacao)
    linha = largura * "-"
    tabela_classificacao = linha + "\n" + tabela_classificacao + linha + "\n"

    # ordenar os jogadores por pontos
    ranking = sorted(jogadores.items(), key=lambda x: x[1]["pontos"], reverse=True)

    for _, valores in ranking:
        nome = valores["nome"]
        pontos = str(valores["pontos"])
        tabela_classificacao += f"{nome.ljust(10)} | {pontos.rjust(2)}\n"
    
    return tabela_classificacao


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    print('\n--- Iniciando Jogo - Stop ---\n')
    n_rodada_atual = 1

    # loop das conexoes
    while len(jogadores) < NUM_JOGADORES:
        # recebe conexao do cliente
        conn, addr = s.accept()
        
        # verifica se tem dados
        data = conn.recv(1024)
        if not data:
            conn.close()
            continue

        # salva o jogador
        jogadores[conn] = {
            "nome": data.decode().strip(),
            "pontos": 0
        }

    
    # loop do jogo
    while n_rodada_atual <= N_RODADAS:
    
        # apos todos os jogadores se conectarem, enviar a letra
        letra_sorteada = chr(randint(65, 90)) # sorteia letras no intervalo [A-Z]
        for conn in jogadores:
            # mensagem = f"Bem vindo, {jogadores[conn]['nome']}\n"
            mensagem = f"Letra: {letra_sorteada}"
            conn.sendall(mensagem.encode())
        
        # receber as palavras enviadas
        print(">_ for -> thread.start/join()")
        for conn in jogadores:
            thread = threading.Thread(target=salvar_respostas_jogador, args=(conn,))
            thread.start()
            thread.join()
        

        # calcular resultado
        print(">_ calcular_pontuacao()")
        calcular_pontuacao()


        # envia placar aos jogadores
        time.sleep(WAITING_TIME)
        for conn in jogadores:
            mensagem = f"Resultado da rodada {n_rodada_atual}:\n"
            mensagem += f"Pontuação: {jogadores[conn]["pontos"]} pontos"
            conn.sendall(mensagem.encode())

        # atualiza contador das rodadas
        n_rodada_atual += 1

    
    # enviar placar final a todos os jogadores    
    tabela_classificacao = criar_tabela_classificacao()
    
    print(tabela_classificacao)
    for conn in jogadores:
        conn.sendall(tabela_classificacao.encode())

    
