from socket import *
from threading import Thread

HOST = "0.0.0.0"
PORT = 5000


def processar_requisicao(conn, addr, requisicao):
    """
    Processa uma requisição em uma thread separada.
    """

    try:
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

    finally:
        conn.close()


# Cria um socket TCP
s = socket(AF_INET, SOCK_STREAM)

# Permite reutilizar a porta após reiniciar o servidor
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Associa o socket ao endereço e à porta
s.bind((HOST, PORT))

# Permite várias conexões aguardando atendimento
s.listen(128)

print(f"Servidor multithread aguardando conexões em {HOST}:{PORT}...")


while True:
    # A thread principal aceita uma nova conexão
    conn, addr = s.accept()

    # Recebe a requisição
    data = conn.recv(1024)

    if not data:
        conn.close()
        continue

    requisicao = data.decode()

    # Cria uma nova thread para processar a requisição
    thread = Thread(
        target=processar_requisicao,
        args=(conn, addr, requisicao)
    )

    thread.start()