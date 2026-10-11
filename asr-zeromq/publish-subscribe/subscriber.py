import zmq, argparse
from constPS import * #-

parser = argparse.ArgumentParser(description="Subscriber (ZeroMQ)")
parser.add_argument("topicos", nargs="*", default=["TIME"],
                    help="tópicos a assinar: TIME, TEMP, UMID, ALERTA (padrão: TIME)")
parser.add_argument("-n", type=int, default=5,
                    help="quantas mensagens receber; 0 = até Ctrl+C (padrão: 5)")
args = parser.parse_args()

context = zmq.Context()
s = context.socket(zmq.SUB)          # create a subscriber socket
p = "tcp://" + HOST + ":" + PORT     # how and where to communicate
s.connect(p)                         # connect to the server
for topico in args.topicos:          # o filtro é feito pelo prefixo da mensagem
    s.setsockopt_string(zmq.SUBSCRIBE, topico.upper())

print("Assinando " + ", ".join(t.upper() for t in args.topicos) + " em " + p)

ultimo = {}                          # tópico -> último número de sequência visto
recebidas = perdidas = 0
try:
    while args.n == 0 or recebidas < args.n:
        msg = bytes.decode(s.recv())             # receive a message
        topico, seq, conteudo = msg.split(" ", 2)
        seq = int(seq)
        if topico in ultimo and seq > ultimo[topico] + 1:
            faltam = seq - ultimo[topico] - 1
            perdidas += faltam
            print("  (%d mensagem(ns) de %s perdida(s))" % (faltam, topico))
        ultimo[topico] = seq
        recebidas += 1
        print("[%s #%d] %s" % (topico, seq, conteudo))
except KeyboardInterrupt:
    pass

print("Recebidas: %d | perdidas detectadas: %d" % (recebidas, perdidas))
for topico, seq in sorted(ultimo.items()):
    print("  %s: última mensagem foi a #%d" % (topico, seq))
