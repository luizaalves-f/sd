# compara o tamanho das mensagens e o tempo de resposta dos exemplos restful
# e grpc do professor. os servidores sao executados sem alteraçoes
#
# uso (a partir desta pasta com venv ativo):
#   python medicao.py [-n REQUISICOES] [-f FUNCIONARIOS]

import argparse, json, os, statistics, subprocess, sys, time

import grpc
import requests
from grpc_tools import protoc

AQUI    = os.path.dirname(os.path.abspath(__file__))
ASR12   = os.path.dirname(AQUI)
REST    = os.path.join(ASR12, "RESTful-WS-Example")
GRPC    = os.path.join(ASR12, "gRPC-WS-Example", "python")
PROTOS  = os.path.join(ASR12, "gRPC-WS-Example", "protos")
GERADOS = os.path.join(AQUI, "gerados")     # stubs gerados a partir do .proto

URL_REST = "http://127.0.0.1:5678/empdb/employee"
END_GRPC = "127.0.0.1:50051"

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, default=1000, help="requisições por medição (padrão: 1000)")
parser.add_argument("-f", type=int, default=1000, help="funcionários na lista grande (padrão: 1000)")
args = parser.parse_args()

# 1. gera os stubs do grpc

os.makedirs(GERADOS, exist_ok=True)
protoc.main(["protoc", "-I" + PROTOS, "--python_out=" + GERADOS,
             "--grpc_python_out=" + GERADOS, os.path.join(PROTOS, "EmployeeService.proto")])
sys.path.insert(0, GERADOS)
import EmployeeService_pb2 as pb
import EmployeeService_pb2_grpc as pb_grpc

# 2. sobe os dois servidores do professor
ambiente = dict(os.environ, PYTHONPATH=GERADOS)
servidores = [
    subprocess.Popen([sys.executable, "EmployeeService.py"], cwd=REST,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
    subprocess.Popen([sys.executable, "EmployeeService.py"], cwd=GRPC, env=ambiente,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
]


def esperar_servidores():
    for _ in range(50):
        try:
            requests.get(URL_REST, timeout=1)
            grpc.channel_ready_future(grpc.insecure_channel(END_GRPC)).result(timeout=1)
            return
        except Exception:
            time.sleep(0.2)
    sys.exit("Os servidores não subiram")


def cronometrar(funcao, n=None):
    """Executa a função n vezes (padrão: args.n) e devolve a mediana do tempo
    em milissegundos. A mediana é menos afetada por picos ocasionais que a média."""
    for _ in range(50):                     # aquecimento
        funcao()
    tempos = []
    for _ in range(n or args.n):
        inicio = time.perf_counter()
        funcao()
        tempos.append((time.perf_counter() - inicio) * 1000)
    return statistics.median(tempos)


def tamanho_cabecalhos_http(resposta):
    """Bytes da linha de requisição/status e dos cabeçalhos HTTP/1.1, ida e volta."""
    req = resposta.request
    ida = len("%s %s HTTP/1.1\r\n" % (req.method, req.path_url))
    ida += sum(len("%s: %s\r\n" % kv) for kv in req.headers.items()) + 2
    volta = len("HTTP/1.1 %d %s\r\n" % (resposta.status_code, resposta.reason))
    volta += sum(len("%s: %s\r\n" % kv) for kv in resposta.headers.items()) + 2
    return ida + volta


try:
    esperar_servidores()
    sessao = requests.Session()             # reaproveita a conexao tcp como o canal grpc
    canal = grpc.insecure_channel(END_GRPC)
    stub = pb_grpc.EmployeeServiceStub(canal)

    # 3. tamanho das mensagens
    um_rest = sessao.get(URL_REST + "/101")
    um_grpc = stub.GetEmployeeDataFromID(pb.EmployeeID(id=101))
    lista_rest = sessao.get(URL_REST)
    lista_grpc = stub.ListAllEmployees(pb.EmptyMessage())

    # mesmos dados (id numerico, nome e cargo) nos dois formatos, para comparar so o formato
    registros = [{"id": e.id, "name": e.name, "title": e.title} for e in lista_grpc.employee_data]
    mesmo_json = len(json.dumps({"employee_data": registros}, separators=(",", ":")).encode())

    print("\n=== Tamanho das mensagens (bytes) ===")
    print("%-42s %10s %10s" % ("", "RESTful", "gRPC"))
    print("%-42s %10d %10d" % ("Consultar 1 funcionário (corpo da resposta)",
                               len(um_rest.content), um_grpc.ByteSize()))
    print("%-42s %10d %10d" % ("Listar 2 funcionários (corpo da resposta)",
                               len(lista_rest.content), lista_grpc.ByteSize()))
    print("%-42s %10d %10d" % ("Mesmos 2 registros, so id/nome/cargo",
                               mesmo_json, lista_grpc.ByteSize()))
    print("Cabeçalhos HTTP/1.1 de uma requisiçao RESTful (ida e volta): %d bytes"
          % tamanho_cabecalhos_http(um_rest))

    # 4. tempo por requisiçao com a lista pequena
    print("\n=== Mediana do tempo por requisição (ms, %d requisições) ===" % args.n)
    print("%-42s %10s %10s" % ("", "RESTful", "gRPC"))
    t_um = (cronometrar(lambda: sessao.get(URL_REST + "/101").json()),
            cronometrar(lambda: stub.GetEmployeeDataFromID(pb.EmployeeID(id=101))))
    print("%-42s %10.3f %10.3f" % ("Consultar 1 funcionário", *t_um))
    t_lista = (cronometrar(lambda: sessao.get(URL_REST).json()),
               cronometrar(lambda: stub.ListAllEmployees(pb.EmptyMessage())))
    print("%-42s %10.3f %10.3f" % ("Listar 2 funcionários", *t_lista))
    # so 200 chamadas: cada uma abre uma conexao tcp nova e muitas seguidas
    # esgotam as portas locais disponiveis (erro 10048 no windows)
    t_nova = cronometrar(lambda: requests.get(URL_REST + "/101").json(), n=200)
    print("%-42s %10.3f %10s" % ("Consultar 1, nova conexão (200 chamadas)", t_nova, "-"))

    # 5. mesma comparaçao com uma lista grande
    for i in range(1000, 1000 + args.f - 2):
        sessao.post(URL_REST, json={"id": str(i), "name": "Funcionario %d" % i,
                                    "title": "Programador"})
        stub.CreateEmployee(pb.EmployeeData(id=i, name="Funcionario %d" % i, title="Programador"))
    grande_rest = sessao.get(URL_REST)
    grande_grpc = stub.ListAllEmployees(pb.EmptyMessage())
    n_lista = len(grande_grpc.employee_data)
    t_grande = (cronometrar(lambda: sessao.get(URL_REST).json()),
                cronometrar(lambda: stub.ListAllEmployees(pb.EmptyMessage())))

    print("\n=== Lista com %d funcionarios ===" % n_lista)
    print("%-42s %10s %10s" % ("", "RESTful", "gRPC"))
    print("%-42s %10d %10d" % ("Tamanho do corpo da resposta (bytes)",
                               len(grande_rest.content), grande_grpc.ByteSize()))
    print("%-42s %10.3f %10.3f" % ("Mediana do tempo por requisiçao (ms)", *t_grande))
finally:
    for s in servidores:
        s.terminate()
