import zmq, pickle
from constPipe import *  #-

OCIOSO_MS = 5000    # sem resultados por esse tempo -> imprime o resumo parcial

context = zmq.Context()
r = context.socket(zmq.PULL)      # recebe os resultados de todos os workers
r.bind("tcp://*:" + PORT3)

por_worker = {}                   # worker -> [tarefas, carga total, tempo total]
por_fonte  = {}                   # fonte  -> tarefas concluídas
primos = []


def resumo():
    total = sum(v[0] for v in por_worker.values())
    print("\n===== Resumo: %d tarefas concluidas =====" % total)
    for w, (n, carga, tempo) in sorted(por_worker.items()):
        print("  worker %-8s %3d tarefas (%5.1f%%) | carga total %4d | %.2fs trabalhando"
              % (w, n, 100.0 * n / total, carga, tempo))
    for f, n in sorted(por_fonte.items()):
        print("  fonte %s: %d tarefas" % (f, n))
    print("  cargas primas encontradas: %d %s\n" % (len(primos), sorted(set(primos))))


print("Sink na porta " + PORT3 + " (Ctrl+C para encerrar)")
pendente = False                  # há resultados ainda não resumidos?
try:
    while True:
        if not r.poll(OCIOSO_MS):
            if pendente:
                resumo()
                pendente = False
            continue
        worker, fonte, tarefa, carga, primo, duracao = pickle.loads(r.recv())
        w = por_worker.setdefault(worker, [0, 0, 0.0])
        w[0] += 1
        w[1] += carga
        w[2] += duracao
        por_fonte[fonte] = por_fonte.get(fonte, 0) + 1
        if primo:
            primos.append(carga)
        pendente = True
        print("%s concluiu tarefa %d da fonte %s (carga %d%s) em %.2fs"
              % (worker, tarefa, fonte, carga, ", primo" if primo else "", duracao))
except KeyboardInterrupt:
    if por_worker:
        resumo()
    print("Sink encerrado")
