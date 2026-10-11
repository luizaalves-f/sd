import zmq, argparse, sys
from constCS import * #-

parser = argparse.ArgumentParser(description="Cliente request-reply (ZeroMQ)")
parser.add_argument("--porta", choices=["1", "2"], default="1",
                    help="qual das duas portas do servidor usar (padrão: 1)")
parser.add_argument("comando", nargs="*",
                    help="ex.: UPPER ola mundo. Sem comando, roda uma demonstração")
args = parser.parse_args()

context = zmq.Context()
p = "tcp://" + HOST + ":" + (PORT1 if args.porta == "1" else PORT2)


def conectar():
    s = context.socket(zmq.REQ)     # create request socket
    s.setsockopt(zmq.LINGER, 0)     # não segura mensagens pendentes ao fechar
    s.connect(p)
    return s


def requisitar(s, texto):
    """Envia a requisição e espera a resposta com timeout. Se o servidor não
    responder, descarta o socket (um REQ fica travado esperando a resposta) e
    tenta de novo com um socket novo. Retorna (socket, resposta)."""
    for tentativa in range(1, TENTATIVAS + 1):
        s.send(str.encode(texto))
        if s.poll(TIMEOUT_MS):
            return s, bytes.decode(s.recv())
        print("  sem resposta (tentativa %d de %d)" % (tentativa, TENTATIVAS))
        s.close()
        s = conectar()
    return s, None


if args.comando:
    requisicoes = [" ".join(args.comando)]
else:
    requisicoes = [
        "ECHO Hello world " + args.porta,
        "UPPER sistemas distribuidos",
        "REVERSE Sistemas Distribuidos",
        "COUNT Sistemas Distribuidos",
        "TIME",
        "STATS",
    ]

s = conectar()
print("Conectado a " + p)
for texto in requisicoes:
    s, resposta = requisitar(s, texto)
    if resposta is None:
        print("Servidor indisponível, desistindo.")
        s.close()
        sys.exit(1)
    print(texto + " -> " + resposta)
s.close()
