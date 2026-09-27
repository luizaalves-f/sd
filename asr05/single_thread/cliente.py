from socket import *
import random
import string
import time
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("IP_DO_PEER01")
PORT = 5000

NUM_REQUISICOES = 1000
TAMANHO_TEXTO = 100
SEED = 42


def gerar_requisicoes():

    random.seed(SEED)

    requisicoes = []

    for _ in range(NUM_REQUISICOES):

        operacao = str(random.randint(1, 3))

        texto = "".join(
            random.choices(
                string.ascii_letters + string.digits,
                k=TAMANHO_TEXTO
            )
        )

        requisicoes.append(f"{operacao}|{texto}")

    return requisicoes


def enviar_requisicao(requisicao):

    s = socket(AF_INET, SOCK_STREAM)

    try:
        s.connect((HOST, PORT))

        s.sendall(requisicao.encode())

        resposta = s.recv(1024)

    finally:
        s.close()


requisicoes = gerar_requisicoes()

print(f"Enviando {NUM_REQUISICOES} requisições...")


inicio = time.perf_counter()


# Envia uma requisição por vez
for requisicao in requisicoes:
    enviar_requisicao(requisicao)


fim = time.perf_counter()

tempo_total = fim - inicio


print("\nExperimento concluído.")
print(f"Quantidade de requisições: {NUM_REQUISICOES}")
print(f"Tempo total: {tempo_total:.4f} segundos")
print(
    f"Requisições por segundo: "
    f"{NUM_REQUISICOES / tempo_total:.2f}"
)