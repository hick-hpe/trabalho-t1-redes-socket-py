import socket
import json

HOST = '127.0.0.1'
PORT = 9000

N_RODADAS = 2
n_rodada_atual = 1
FORMATO_CODIFICACAO = 'UTF-8'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # enviar nome ao servidor
    nome = input("Nome: ")
    s.sendall(nome.encode(FORMATO_CODIFICACAO))

    # salva a lista de temas do servidor
    temas = json.loads(s.recv(1024).decode(FORMATO_CODIFICACAO))

    while n_rodada_atual <= N_RODADAS:
        # recebe resposta
        resposta = s.recv(1024).decode(FORMATO_CODIFICACAO)

        # enviar respostas
        print(
            f"\nRodada {n_rodada_atual}\n"
            f"{resposta}\n"
            "Envie suas respostas!!"
        )

        # jogador envia suas respostas
        for tema in temas:
            valor = input(f"{tema}:")

            # salvar em json
            obj = {
                tema: valor
            }

            # enviar ao servidor
            obj_str = json.dumps(obj)
            s.sendall(obj_str.encode(FORMATO_CODIFICACAO))

            # servidor diz se pode continuar ou nao a enviar respostas
            print('esperando "pode_continuar" do server...')
            pode_continuar = json.loads(s.recv(1024).decode(FORMATO_CODIFICACAO))
            
            if not pode_continuar:
                print("Servidor nao recebe mais respostas!!!")
                break

        # pontuacao da rodada
        print('esperando "pontuacao da rodada" do server...')
        resposta = s.recv(1024).decode(FORMATO_CODIFICACAO)
        print(f"\n{resposta}")

        n_rodada_atual += 1


    # aguardar classificacao geral
    tabela_classificacao = s.recv(1024).decode(FORMATO_CODIFICACAO)
    print(f"\n{tabela_classificacao}")

