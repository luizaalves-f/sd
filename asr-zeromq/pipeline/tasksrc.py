import zmq, time, pickle, sys, random
from constPipe import * #-

if len(sys.argv) < 2 or sys.argv[1] not in ("1", "2"):
    sys.exit("Uso: python tasksrc.py <1|2> [quantidade de tarefas] [intervalo em s]")

me        = sys.argv[1]
total     = int(sys.argv[2]) if len(sys.argv) > 2 else 100
intervalo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

context = zmq.Context()
s   = context.socket(zmq.PUSH)        # create a push socket
prt = PORT1 if me == '1' else PORT2   # check task source port
s.bind("tcp://*:" + prt)              # escuta em todas as interfaces

print("Fonte " + me + " na porta " + prt + ": gerando " + str(total) + " tarefas")

for i in range(1, total + 1):         # generate workloads
    time.sleep(intervalo)
    workload = random.randint(1, 100)       # compute workload
    s.send(pickle.dumps((me, i, workload))) # send workload to worker
    print("Fonte %s enviou tarefa %d (carga %d)" % (me, i, workload))

print("Fonte " + me + " terminou")
s.close()
context.term()                        # espera as tarefas pendentes serem entregues
