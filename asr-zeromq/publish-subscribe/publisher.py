import zmq, time, random
from constPS import * #-

context = zmq.Context()
s = context.socket(zmq.PUB)        # create a publisher socket
s.bind("tcp://*:" + PORT)          # escuta em todas as interfaces

seq = {}                           # tópico -> número da última mensagem


def publicar(topico, conteudo):
    # Formato: "<TOPICO> <seq> <conteudo>". O número de sequência por tópico
    # permite ao subscriber perceber quando perdeu mensagens.
    seq[topico] = seq.get(topico, 0) + 1
    msg = "%s %d %s" % (topico, seq[topico], conteudo)
    s.send(str.encode(msg))
    print("Publicado: " + msg)


print("Publisher na porta " + PORT + " (Ctrl+C para encerrar)")
temperatura = 27.0
try:
    while True:
        time.sleep(1)
        publicar("TIME", time.asctime())

        temperatura += random.uniform(-1.5, 1.5)      # sensor simulado
        temperatura = min(max(temperatura, 20.0), 35.0)
        publicar("TEMP", "%.1f" % temperatura)
        publicar("UMID", "%d" % random.randint(30, 80))

        if temperatura > LIMITE_ALERTA:
            publicar("ALERTA", "temperatura alta: %.1f C" % temperatura)
except KeyboardInterrupt:
    print("Publisher encerrado")
