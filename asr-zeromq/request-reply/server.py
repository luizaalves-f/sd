import zmq, time
from constCS import * #-

context = zmq.Context()

s = context.socket(zmq.REP)         # create reply socket
s.bind("tcp://*:" + PORT1)          # escuta em todas as interfaces,
s.bind("tcp://*:" + PORT2)          # nas duas portas

inicio = time.time()
atendidas = {}                      # comando -> quantidade de requisições


def processar(comando, argumento):
    if comando == "ECHO":           # comportamento original do exemplo
        return argumento + "*"
    if comando == "UPPER":
        return argumento.upper()
    if comando == "REVERSE":
        return argumento[::-1]
    if comando == "COUNT":
        return str(len(argumento))
    if comando == "TIME":
        return time.asctime()
    if comando == "STATS":
        total = sum(atendidas.values())
        detalhe = ", ".join(c + "=" + str(n) for c, n in sorted(atendidas.items()))
        return "%d requisicoes em %.0fs (%s)" % (total, time.time() - inicio, detalhe)
    return "ERRO: comando desconhecido '" + comando + "'"


print("Servidor aguardando nas portas " + PORT1 + " e " + PORT2)

while True:
    msg = bytes.decode(s.recv())            # wait for incoming message
    comando, _, argumento = msg.partition(" ")
    comando = comando.upper()
    atendidas[comando] = atendidas.get(comando, 0) + 1
    print("Recebido: " + msg)

    if comando == "STOP":
        s.send(b"Servidor encerrado")       # REQ/REP exige uma resposta
        break
    s.send(str.encode(processar(comando, argumento)))

s.close()
context.term()                              # garante o envio da última resposta
