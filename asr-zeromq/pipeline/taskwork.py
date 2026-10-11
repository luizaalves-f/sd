import zmq, time, pickle, sys
from constPipe import *  #-

if len(sys.argv) < 2:
    sys.exit("Uso: python taskwork.py <nome do worker>")

context = zmq.Context()
me = str(sys.argv[1])
r  = context.socket(zmq.PULL)     # create a pull socket
p1 = "tcp://"+ SRC1 +":"+ PORT1   # address first task source
p2 = "tcp://"+ SRC2 +":"+ PORT2   # address second task source
r.connect(p1)                     # connect to task source 1
r.connect(p2)                     # connect to task source 2

out = context.socket(zmq.PUSH)    # resultados seguem para o sink
out.connect("tcp://" + SINK + ":" + PORT3)


def eh_primo(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


print (me + " started")

try:
    while True:
        fonte, tarefa, carga = pickle.loads(r.recv())   # receive work from a source
        print (me + " received " + str(carga) + " from " + fonte)
        inicio = time.time()
        time.sleep(carga * 0.01)                        # pretend to work
        primo = eh_primo(carga)
        duracao = time.time() - inicio
        out.send(pickle.dumps((me, fonte, tarefa, carga, primo, duracao)))
except KeyboardInterrupt:
    print(me + " encerrado")
