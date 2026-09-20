from socket import *

HOST = "127.0.0.1"
PORT = 5000

# Cria um socket TCP
s = socket(AF_INET, SOCK_STREAM)

# Associa o socket ao endereço e à porta definidos
s.bind((HOST, PORT))

# Coloca o servidor em modo de escuta
s.listen(1)

print(f"Servidor aguardando conexão em {HOST}:{PORT}...")

# Aguarda a conexão de um cliente
conn, addr = s.accept()

print(f"Cliente conectado: {addr}")

# Mantém o servidor disponível para receber várias requisições do cliente
while True:
    # Recebe os dados enviados pelo cliente
    data = conn.recv(1024)

    # Encerra caso a conexão seja fechada pelo cliente
    if not data:
        break

    requisicao = data.decode()

    # Encerra a comunicação quando o cliente solicita a saída
    if requisicao == "SAIR":
        break

    # Separa a operação do texto recebido
    operacao, texto = requisicao.split("|", 1)

    # Processa a requisição de acordo com a operação escolhida
    if operacao == "1":
        resposta = texto.upper()

    elif operacao == "2":
        resposta = texto[::-1]

    elif operacao == "3":
        resposta = str(len(texto))

    else:
        resposta = "Operação inválida"

    # Envia o resultado do processamento de volta ao cliente
    conn.send(resposta.encode())

# Fecha a conexão com o cliente e o socket do servidor
conn.close()
s.close()