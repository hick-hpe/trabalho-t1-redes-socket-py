# Grupo de Mensagens

📄 📌 Documentação — enviar_mensagem.py
🧩 Descrição geral

O arquivo enviar_mensagem.py implementa um cliente de envio de mensagens para o ChatServer.
Ele é responsável por:

Conectar ao servidor via socket TCP
Registrar o nome do usuário
Enviar mensagens continuamente ao servidor
⚙️ Configurações iniciais
HOST = "127.0.0.1"
PORT = 9000
HOST: endereço do servidor (localhost)
PORT: porta onde o servidor está escutando
🔌 Conexão com o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
Cria um socket TCP (SOCK_STREAM)
Conecta ao servidor definido em HOST e PORT
👤 Registro do usuário
nome = input(": ")
s.sendall(f"/nome {nome}".encode())
O cliente solicita o nome do usuário
Envia ao servidor com o comando especial /nome
O servidor usa isso para identificar o cliente
✅ Confirmação de login
resposta_login = s.recv(1024).decode()
Aguarda resposta do servidor (ex: "OK")
Confirma que o usuário foi registrado com sucesso
💬 Envio de mensagens
while True:
    mensagem = input(": ")
    s.sendall(mensagem.encode())
Loop infinito para envio de mensagens
Cada mensagem digitada é enviada ao servidor
🛑 Tratamento de saída
except KeyboardInterrupt:
    print("You left the game")
Permite sair com CTRL + C
Evita erro abrupto no programa
🔄 Fluxo de execução
Conecta ao servidor
Solicita nome do usuário
Envia /nome
Aguarda confirmação
Entra em loop enviando mensagens
⚠️ Possíveis melhorias
Validar nome vazio
Mostrar confirmação do servidor
Adicionar comando /sair
Tratar desconexão do servidor
📄 📌 Documentação — listar_mensagem.py
🧩 Descrição geral

Este arquivo implementa um cliente leitor de mensagens do ChatServer.

Função principal:

Solicitar mensagens ao servidor
Exibir mensagens formatadas
⚙️ Configuração
HOST = "127.0.0.1"
PORT = 9000
🔌 Conexão
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
🔁 Loop de leitura
while True:
    s.sendall(b"/listar")
Envia o comando /listar ao servidor
Solicita mensagens disponíveis
📥 Recebimento de dados
data = s.recv(1024)
mensagem = json.loads(data.decode())
Recebe resposta do servidor
Converte JSON → objeto Python
📤 Exibição
print(f"{mensagem}\n")
Mostra a mensagem no terminal
🔄 Fluxo
Conecta ao servidor
Envia /listar
Recebe mensagem
Exibe
Repete
⚠️ Melhorias
Adicionar delay (evitar flood no servidor)
Tratar erro de JSON
Mostrar mensagens formatadas melhor
Parar loop com comando
📄 📌 Documentação — servidor.py
🧩 Descrição geral

Arquivo principal do sistema. Implementa um servidor de chat concorrente utilizando:

Sockets TCP
Threads
Semáforos (controle de concorrência)
🌐 Configuração
HOST = "0.0.0.0"
PORT = 9000
0.0.0.0: aceita conexões de qualquer IP
📦 Estruturas de dados
usuarios = {}
mensagens = []
usuarios: armazena nome e IP por conexão
mensagens: fila de mensagens
🔐 Controle de concorrência
SEMAFORO_ACESSO = threading.Semaphore(1)
SEMAFORO_MENSAGENS = threading.Semaphore(0)
SEMAFORO_ACESSO: controla acesso à lista de mensagens
SEMAFORO_MENSAGENS: indica se há mensagens disponíveis
📨 Função: acessar mensagens
def acessar_mensagem_recente(conn):
Função:
Espera existir mensagem
Remove da fila
Envia ao cliente
Fluxo:
Aguarda mensagem (SEMAFORO_MENSAGENS)
Bloqueia acesso
Remove mensagem
Libera acesso
Envia ao cliente
🧾 Função: formatar mensagem
def formatar_mensagem(conn, mensagem):
Retorna:

Mensagem formatada com:

Nome
IP
Horário

Exemplo:

[David (127.0.0.1) 14:32:10]
Olá mundo
👤 Função: registrar usuário
def registrar_usuario(conn, addr, data):
Função:
Extrai nome do comando /nome
Armazena no dicionário usuarios
Envia "OK"
💾 Função: salvar mensagem
def salvar_mensagem(conn, data):
Função:
Recebe mensagem
Formata
Adiciona à fila
Libera semáforo de mensagens
🔄 Thread principal de cliente
def receber_dados_socket(conn, addr):
Função:

Gerencia comunicação com cada cliente

Regras:
/listar → envia mensagem
/nome → registra usuário
outro → salva mensagem
🧵 Threads
threading.Thread(target=receber_dados_socket)
Cada cliente roda em uma thread separada
Permite múltiplos usuários simultâneos
🚀 Inicialização do servidor
s.bind((HOST, PORT))
s.listen()
Inicia servidor
Aguarda conexões
🔁 Loop principal
while True:
    conn, addr = s.accept()
Aceita conexões
Cria thread para cada cliente
⚠️ Pontos críticos
Uso correto de semáforos evita:
race condition
corrupção da lista
⚠️ Melhorias possíveis
Remover usuário ao desconectar
Broadcast (enviar para todos)
Persistência (banco de dados)
Melhor tratamento de erro
Logs mais organizados
🧠 Resumo do sistema
enviar_mensagem.py → cliente que envia mensagens
listar_mensagem.py → cliente que lê mensagens
servidor.py → servidor central com controle de concorrência
