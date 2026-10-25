# Funções usadas pelos dois servidores de aplicação: iniciar o servidor gRPC,
# registrar o endereço no serviço de nomes e remover o registro ao encerrar.
from concurrent import futures
import socket, sys

import grpc
import nomes_pb2
import nomes_pb2_grpc

import config


def descobrir_ip():
    if config.IP_PROPRIO:
        return config.IP_PROPRIO
    # Um socket UDP "conectado" não envia nada pela rede, mas faz o sistema
    # escolher a interface de saída; getsockname() devolve o IP dela.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((config.IP_NOMES, int(config.PORTA_NOMES)))
        return s.getsockname()[0]
    finally:
        s.close()


def conectar_nomes():
    canal = grpc.insecure_channel(config.IP_NOMES + ":" + config.PORTA_NOMES)
    return canal, nomes_pb2_grpc.ServicoNomesStub(canal)


def registrar(nome, ip, porta):
    canal, stub = conectar_nomes()
    with canal:
        msg = nomes_pb2.BindMsg(nome=nome, endereco=nomes_pb2.EnderecoMsg(ip=ip, porta=porta))
        resposta = stub.Bind(msg, timeout=config.TIMEOUT)
        operacao = "bind"
        if resposta.status == "NOK":
            # o nome já existe (por exemplo, o serviço mudou de máquina): atualiza o endereço
            resposta = stub.Rebind(msg, timeout=config.TIMEOUT)
            operacao = "rebind"
    print("%s de %s -> %s:%s: %s (%s)" % (operacao, nome, ip, porta,
                                          resposta.status, resposta.mensagem))


def remover(nome, ip, porta):
    canal, stub = conectar_nomes()
    with canal:
        # só remove se o registro ainda for deste servidor; se outro servidor
        # fez rebind do mesmo nome, o registro dele é mantido
        atual = stub.Lookup(nomes_pb2.NomeMsg(nome=nome), timeout=config.TIMEOUT)
        if atual.status == "NOK":
            print("%s já não estava registrado" % nome)
            return
        if (atual.endereco.ip, atual.endereco.porta) != (ip, porta):
            print("%s agora aponta para %s:%s, registro mantido"
                  % (nome, atual.endereco.ip, atual.endereco.porta))
            return
        resposta = stub.Unbind(nomes_pb2.NomeMsg(nome=nome), timeout=config.TIMEOUT)
    print("unbind de %s: %s (%s)" % (nome, resposta.status, resposta.mensagem))


def executar_servidor(nome, porta, adicionar_servico):
    """Sobe o servidor gRPC na porta, registra no serviço de nomes e,
    ao receber Ctrl+C, remove o registro e encerra."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    adicionar_servico(server)
    server.add_insecure_port("[::]:" + porta)
    server.start()
    print("%s na porta %s" % (nome, porta))

    ip = descobrir_ip()
    try:
        registrar(nome, ip, porta)
    except grpc.RpcError:
        print("Serviço de nomes indisponível em %s:%s" % (config.IP_NOMES, config.PORTA_NOMES))
        server.stop(0)
        sys.exit(1)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        try:
            remover(nome, ip, porta)
        except grpc.RpcError:
            print("Serviço de nomes indisponível, registro não removido")
        server.stop(0)
        print(nome + " encerrado")
