import grpc
import nomes_pb2
import nomes_pb2_grpc

import config


def endereco(ip, porta):
    return nomes_pb2.EnderecoMsg(ip=ip, porta=porta)


def mostrar(operacao, resposta):
    texto = "%-28s %s (%s)" % (operacao, resposta.status, resposta.mensagem)
    if hasattr(resposta, "endereco") and resposta.status == "OK":
        texto += " -> %s:%s" % (resposta.endereco.ip, resposta.endereco.porta)
    print(texto)


with grpc.insecure_channel(config.IP_NOMES + ":" + config.PORTA_NOMES) as canal:
    stub = nomes_pb2_grpc.ServicoNomesStub(canal)
    nome = "ServicoTeste"

    # casos normais
    mostrar("bind", stub.Bind(nomes_pb2.BindMsg(nome=nome, endereco=endereco("10.0.0.1", "5679"))))
    mostrar("lookup", stub.Lookup(nomes_pb2.NomeMsg(nome=nome)))
    mostrar("rebind", stub.Rebind(nomes_pb2.BindMsg(nome=nome, endereco=endereco("10.0.0.2", "5680"))))
    mostrar("lookup após rebind", stub.Lookup(nomes_pb2.NomeMsg(nome=nome)))
    mostrar("unbind", stub.Unbind(nomes_pb2.NomeMsg(nome=nome)))

    # casos de erro (tratados pelo nosso servidor)
    mostrar("lookup após unbind", stub.Lookup(nomes_pb2.NomeMsg(nome=nome)))
    mostrar("unbind de nome inexistente", stub.Unbind(nomes_pb2.NomeMsg(nome=nome)))
    mostrar("rebind de nome inexistente", stub.Rebind(nomes_pb2.BindMsg(nome=nome, endereco=endereco("10.0.0.3", "5681"))))
    stub.Bind(nomes_pb2.BindMsg(nome=nome, endereco=endereco("10.0.0.1", "5679")))
    mostrar("bind de nome repetido", stub.Bind(nomes_pb2.BindMsg(nome=nome, endereco=endereco("10.0.0.9", "5690"))))
    stub.Unbind(nomes_pb2.NomeMsg(nome=nome))
