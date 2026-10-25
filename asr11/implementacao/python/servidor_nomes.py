from concurrent import futures
import threading

import grpc
import nomes_pb2
import nomes_pb2_grpc

import config


class ServicoNomes(nomes_pb2_grpc.ServicoNomesServicer):

    def __init__(self):
        self.registros = {}             # nome -> (ip, porta)
        self.lock = threading.Lock()    # o servidor atende várias requisições ao mesmo tempo

    def Bind(self, request, context):
        with self.lock:
            if request.nome in self.registros:
                print("Bind recusado: " + request.nome + " já registrado")
                return nomes_pb2.StatusMsg(status="NOK",
                                           mensagem="nome já registrado, use rebind")
            self.registros[request.nome] = (request.endereco.ip, request.endereco.porta)
        print("Bind: %s -> %s:%s" % (request.nome, request.endereco.ip, request.endereco.porta))
        return nomes_pb2.StatusMsg(status="OK", mensagem="nome registrado")

    def Lookup(self, request, context):
        with self.lock:
            registro = self.registros.get(request.nome)
        if registro is None:
            print("Lookup: " + request.nome + " não encontrado")
            return nomes_pb2.LookupMsg(status="NOK", mensagem="nome não encontrado")
        print("Lookup: %s -> %s:%s" % (request.nome, registro[0], registro[1]))
        return nomes_pb2.LookupMsg(status="OK", mensagem="nome encontrado",
                                   endereco=nomes_pb2.EnderecoMsg(ip=registro[0],
                                                                  porta=registro[1]))

    def Unbind(self, request, context):
        with self.lock:
            if request.nome not in self.registros:
                print("Unbind recusado: " + request.nome + " não encontrado")
                return nomes_pb2.StatusMsg(status="NOK", mensagem="nome não encontrado")
            del self.registros[request.nome]
        print("Unbind: " + request.nome)
        return nomes_pb2.StatusMsg(status="OK", mensagem="nome removido")

    def Rebind(self, request, context):
        with self.lock:
            if request.nome not in self.registros:
                print("Rebind recusado: " + request.nome + " não encontrado")
                return nomes_pb2.StatusMsg(status="NOK",
                                           mensagem="nome não encontrado, use bind")
            self.registros[request.nome] = (request.endereco.ip, request.endereco.porta)
        print("Rebind: %s -> %s:%s" % (request.nome, request.endereco.ip, request.endereco.porta))
        return nomes_pb2.StatusMsg(status="OK", mensagem="endereço atualizado")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nomes_pb2_grpc.add_ServicoNomesServicer_to_server(ServicoNomes(), server)
    server.add_insecure_port("[::]:" + config.PORTA_NOMES)
    server.start()
    print("Serviço de nomes na porta " + config.PORTA_NOMES)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("Serviço de nomes encerrado")


if __name__ == "__main__":
    serve()
