from socket import *

HOST = "0.0.0.0"
PORT = 5000


s = socket(AF_INET, SOCK_STREAM)

s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(128)

print(f"Servidor single-thread aguardando conexões em {HOST}:{PORT}...")


while True:

    conn, addr = s.accept()

    data = conn.recv(1024)

    if not data:
        conn.close()
        continue

    requisicao = data.decode()

    operacao, texto = requisicao.split("|", 1)

    if operacao == "1":
        resposta = texto.upper()

    elif operacao == "2":
        resposta = texto[::-1]

    elif operacao == "3":
        resposta = str(len(texto))

    else:
        resposta = "Operação inválida"

    conn.sendall(resposta.encode())

    conn.close()