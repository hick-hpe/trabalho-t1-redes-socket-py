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
TEMAS = ["nome", "cep", "fruta", "cor"]
FORMATO_CODIFICACAO = 'UTF-8'
jogadores = {}
jogador_terminou_primeiro = None
SEMAFORO = threading.Semaphore(1)

# calcula a pontuacao dos jogadores
def calcular_pontuacao():
    # organizar as respostas recebidas por temas
    respostas = {t: {} for t in TEMAS}

    # organizar as respostas iguais
    i = 1
    for conn in jogadores:
        # jogador
        jog = jogadores[conn]

        # respostas do jogador (jog["resp"]) por tema
        for tema in jog["resp"]:

            # se a resposta nao esta na lista geral, adicionar a chave do jogador
            resposta = jog["resp"].get(tema, '')
            if resposta not in respostas[tema]:
                respostas[tema][resposta] = [conn]
            else:
                respostas[tema][resposta].append(conn)

        i += 1
    

    # contar os pontos
    print("---------- analise das respostas ----------")
    for tema in respostas:
        for resposta in respostas[tema]:

            lista_jog = respostas[tema][resposta]
            print(f'[{tema}] responderam "{resposta}": {list(jogadores[conn]["nome"] for conn in lista_jog)}')
    
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
    # identificar jogador
    nome = jogadores[conn]["nome"]

    global jogador_terminou_primeiro

    while True:

        # identificar a categoria a ser salva
        print(f'[server] "{nome}" - esperando resposta do jogador...')
        resposta = conn.recv(1024).decode(FORMATO_CODIFICACAO)
        obj_resp = json.loads(resposta)
        categoria = list(obj_resp.keys())[0]

        # definir o jogador que terminou primeiro - estado global
        with SEMAFORO:

            # se já tem vencedor, ignora novas respostas
            if jogador_terminou_primeiro:
                pode_continuar = False

            else:
                pode_continuar = True

                # salvar resposta
                jogadores[conn].setdefault("resp", {})
                jogadores[conn]["resp"][categoria] = obj_resp[categoria]

                print(f'>_ resposta {categoria}="{obj_resp[categoria]}" de "{nome}"...')

                # se terminou agora
                if categoria == TEMAS[-1]:
                    jogador_terminou_primeiro = conn
                    pode_continuar = False
                    print(f'>_ "{nome}" terminou primeiro!!!')
            
        conn.sendall(json.dumps(pode_continuar).encode(FORMATO_CODIFICACAO))

        # se nao pode mais receber respostas, encerra a thread
        if not pode_continuar:
            print("[server] nao pode mais receber respostas")
            break
    
    print(f"[Thread] {nome} espera pontuacao...")


def criar_ranking():
    return sorted(jogadores.items(), key=lambda x: x[1]["pontos"], reverse=True)


def criar_tabela_classificacao():
    tabela_classificacao = f"{'Nome'.ljust(10)} | {'Pontuação'.ljust(2)}\n"
    largura = len(tabela_classificacao)
    linha = largura * "-"
    tabela_classificacao = linha + "\n" + tabela_classificacao + linha + "\n"

    # ordenar os jogadores por pontos
    ranking = criar_ranking()

    for _, valores in ranking:
        nome = valores["nome"]
        pontos = str(valores["pontos"])
        tabela_classificacao += f"{nome.ljust(10)} | {pontos.rjust(2)}\n"
    
    return tabela_classificacao


def iniciar_servidor():
    global jogador_terminou_primeiro

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()

        print('\n--- Iniciando Jogo - Stop ---\n')
        n_rodada_atual = 1

        # loop das conexoes
        while len(jogadores) < NUM_JOGADORES:
            # recebe conexao do cliente
            conn, addr = servidor.accept()
            
            # verifica se tem dados
            data = conn.recv(1024)
            if not data:
                conn.close()
                continue

            # salva o jogador
            jogadores[conn] = {
                "nome": data.decode(FORMATO_CODIFICACAO).strip(),
                "pontos": 0,
            }

            # enviar lista das categorias ao cliente
            conn.sendall(json.dumps(TEMAS).encode(FORMATO_CODIFICACAO))
        
        
        # loop do jogo
        while n_rodada_atual <= N_RODADAS:
            jogador_terminou_primeiro = None
        
            # apos todos os jogadores se conectarem, enviar a letra
            letra_sorteada = chr(randint(65, 90)) # sorteia letras no intervalo [A-Z]
            for conn in jogadores:
                # mensagem = f"Bem vindo, {jogadores[conn]['nome']}\n"
                mensagem = f"Letra: {letra_sorteada}"
                conn.sendall(mensagem.encode(FORMATO_CODIFICACAO))
            
            # receber as palavras enviadas
            threads_respostas = []
            for conn in jogadores:
                thread = threading.Thread(target=salvar_respostas_jogador, args=(conn,))
                thread.start()
                threads_respostas.append(thread)
            
            for thread in threads_respostas:
                thread.join()
                
            # calcular resultado
            print(">_ calcular_pontuacao()")
            calcular_pontuacao()

            # envia placar aos jogadores
            time.sleep(WAITING_TIME)
            for conn in jogadores:
                mensagem = f"Resultado da rodada {n_rodada_atual}:\n"
                mensagem += f"Pontuação: {jogadores[conn]["pontos"]} pontos"
                conn.sendall(mensagem.encode(FORMATO_CODIFICACAO))

            # atualiza contador das rodadas
            n_rodada_atual += 1

        # enviar placar final a todos os jogadores    
        tabela_classificacao = criar_tabela_classificacao()
        
        print(tabela_classificacao)

        for conn in jogadores:
            conn.sendall(tabela_classificacao.encode(FORMATO_CODIFICACAO))


iniciar_servidor()
