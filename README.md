# Trabalho T1 - Sockets Python 

# 🕹️ Jogo Stop - Cliente/Servidor

Este projeto implementa um jogo estilo **Stop (Adedonha)** utilizando:

- Sockets TCP
- Threads
- JSON para comunicação
- Controle de concorrência com semáforo

---

# 🧱 Estrutura do Projeto

| Arquivo       | Função                          |
|--------------|--------------------------------|
| cliente.py   | Cliente jogador                |
| servidor.py  | Servidor do jogo               |

---

📄 cliente.py

🧩 Descrição
Cliente responsável por representar um jogador no jogo.

Permite:
- Conectar ao servidor
- Enviar nome do jogador
- Receber temas
- Enviar respostas por rodada
- Receber pontuação

⚙️ Configuração

python
HOST = '127.0.0.1'
PORT = 9000
N_RODADAS = 2
FORMATO_CODIFICACAO = 'UTF-8'
--------------------------------------------------------------------------------
🔌 Conexão com servidor
cliente.connect((HOST, PORT))

--------------------------------------------------------------------------------
👤 Registro do jogador
nome = input("Nome: ")
cliente.sendall(nome.encode(FORMATO_CODIFICACAO))

Envia nome ao servidor
--------------------------------------------------------------------------------
📥 Recebimento dos temas

temas = json.loads(cliente.recv(1024).decode(FORMATO_CODIFICACAO))

Recebe lista de categorias (ex: nome, cep, fruta)
--------------------------------------------------------------------------------
🔁 Loop de rodadas
while n_rodada_atual <= N_RODADAS:

--------------------------------------------------------------------------------
📩 Receber letra da rodada
resposta = cliente.recv(1024).decode(FORMATO_CODIFICACAO)

Exibe letra sorteada
--------------------------------------------------------------------------------
✍️ Envio de respostas
for tema in temas:
    valor = input(f"{tema}:")
    
Jogador responde cada tema

--------------------------------------------------------------------------------
📦 Envio em JSON
obj = {tema: valor}
cliente.sendall(json.dumps(obj).encode(FORMATO_CODIFICACAO))

--------------------------------------------------------------------------------
⛔ Controle do servidor
pode_continuar = json.loads(cliente.recv(1024).decode(FORMATO_CODIFICACAO))

Define se o jogador pode continuar respondendo

--------------------------------------------------------------------------------
🏆 Resultado da rodada
resposta = cliente.recv(1024).decode(FORMATO_CODIFICACAO)

Recebe pontuação

--------------------------------------------------------------------------------
📊 Classificação final
tabela_classificacao = cliente.recv(1024).decode(FORMATO_CODIFICACAO)

Exibe ranking final

--------------------------------------------------------------------------------

🔄 Fluxo
Conecta ao servidor
Envia nome
Recebe temas
Recebe letra
Envia respostas
Recebe pontuação
Repete rodadas
Recebe ranking final

--------------------------------------------------------------------------------

⚠️ Melhorias
Validar respostas (letra correta)
Melhorar interface do usuário
Tratar desconexão

--------------------------------------------------------------------------------
📄 servidor.py

🧩 Descrição

Servidor responsável por gerenciar o jogo Stop.

Funções:

Receber jogadores
Controlar rodadas
Receber respostas
Calcular pontuação
Enviar ranking

--------------------------------------------------------------------------------

⚙️ Configuração
HOST = '0.0.0.0'
PORT = 9000
NUM_JOGADORES = 3
N_RODADAS = 2
WAITING_TIME = 2
TEMAS = ["nome", "cep"]

--------------------------------------------------------------------------------

📦 Estruturas
jogadores = {}

Cada jogador possui:

nome
pontos
respostas

--------------------------------------------------------------------------------

🔐 Semáforo
SEMAFORO = threading.Semaphore(1)

Controla acesso concorrente

--------------------------------------------------------------------------------

🎯 Função: calcular_pontuacao()
Regra:
Resposta única → 3 pontos
Resposta repetida → 1 ponto

--------------------------------------------------------------------------------

💾 Função: salvar_respostas_jogador(conn)
Função:
Recebe respostas do jogador
Salva por categoria
Define quem terminou primeiro

--------------------------------------------------------------------------------

🧠 Lógica importante
if jogador_terminou_primeiro:

Quando um jogador termina:
Outros são bloqueados

--------------------------------------------------------------------------------

🧵 Threads
threading.Thread(target=salvar_respostas_jogador)

Cada jogador responde em paralelo

--------------------------------------------------------------------------------

🏁 Ranking
Criar ranking:
sorted(jogadores.items(), key=lambda x: x[1]["pontos"])

--------------------------------------------------------------------------------

📊 Tabela final
def criar_tabela_classificacao()

Formato:

----------
Nome       | Pontuação
----------
Ana        | 6
João       | 4

--------------------------------------------------------------------------------

🎮 Loop do jogo
while n_rodada_atual <= N_RODADAS:

Etapas:
Sorteia letra
Envia aos jogadores
Recebe respostas (threads)
Calcula pontuação
Envia resultado

--------------------------------------------------------------------------------

🔤 Sorteio de letra
chr(randint(65, 90))
Letras de A-Z

--------------------------------------------------------------------------------

📤 Envio de resultados
conn.sendall(mensagem.encode())

--------------------------------------------------------------------------------

🏆 Finalização
Envia tabela de classificação para todos os jogadores

--------------------------------------------------------------------------------

⚠️ Pontos importantes
Controle de concorrência com semáforo
Threads para múltiplos jogadores
Uso de JSON para comunicação
--------------------------------------------------------------------------------

⚠️ Melhorias
Validar respostas com a letra
Persistência de dados
Interface gráfica
Timeout para respostas
Melhor tratamento de erros
--------------------------------------------------------------------------------

🧠 Funcionamento geral
Jogadores se conectam
Servidor envia temas
Rodada inicia com letra
Jogadores respondem
Primeiro a terminar bloqueia os outros
Pontuação é calculada
Ranking é atualizado
Após rodadas → resultado final
--------------------------------------------------------------------------------

🛠️ Tecnologias utilizadas
Python
Socket TCP
Threading
JSON
Semáforo
