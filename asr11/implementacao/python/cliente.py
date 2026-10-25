import sys

import grpc
import nomes_pb2
import nomes_pb2_grpc
import calculadora_pb2
import calculadora_pb2_grpc
import texto_pb2
import texto_pb2_grpc

import config


def descobrir(nome):
    """Consulta o serviço de nomes e devolve 'ip:porta' do serviço, ou None."""
    with grpc.insecure_channel(config.IP_NOMES + ":" + config.PORTA_NOMES) as canal:
        stub = nomes_pb2_grpc.ServicoNomesStub(canal)
        resposta = stub.Lookup(nomes_pb2.NomeMsg(nome=nome), timeout=config.TIMEOUT)
    if resposta.status != "OK":
        print("lookup de %s: %s" % (nome, resposta.mensagem))
        return None
    endereco = resposta.endereco.ip + ":" + resposta.endereco.porta
    print("lookup de %s: %s" % (nome, endereco))
    return endereco


def usar_calculadora(endereco):
    with grpc.insecure_channel(endereco) as canal:
        stub = calculadora_pb2_grpc.CalculadoraStub(canal)
        for operacao, a, b in [("Somar", 10, 4), ("Subtrair", 10, 4),
                               ("Multiplicar", 10, 4), ("Dividir", 10, 4), ("Dividir", 1, 0)]:
            resposta = getattr(stub, operacao)(calculadora_pb2.OperandosMsg(a=a, b=b),
                                               timeout=config.TIMEOUT)
            if resposta.status == "OK":
                print("  %s(%g, %g) = %g" % (operacao, a, b, resposta.valor))
            else:
                print("  %s(%g, %g): erro, %s" % (operacao, a, b, resposta.mensagem))


def usar_texto(endereco):
    frase = "Sistemas Distribuidos"
    with grpc.insecure_channel(endereco) as canal:
        stub = texto_pb2_grpc.TextoStub(canal)
        msg = texto_pb2.TextoMsg(texto=frase)
        print("  Inverter('%s') = %s" % (frase, stub.Inverter(msg, timeout=config.TIMEOUT).texto))
        print("  Maiusculas('%s') = %s" % (frase, stub.Maiusculas(msg, timeout=config.TIMEOUT).texto))
        print("  ContarCaracteres('%s') = %d"
              % (frase, stub.ContarCaracteres(msg, timeout=config.TIMEOUT).quantidade))


servicos = [(config.NOME_CALCULADORA, usar_calculadora), (config.NOME_TEXTO, usar_texto)]

print("Serviço de nomes em %s:%s" % (config.IP_NOMES, config.PORTA_NOMES))
for nome, usar in servicos:
    print()
    try:
        endereco = descobrir(nome)
    except grpc.RpcError:
        print("Serviço de nomes indisponível")
        sys.exit(1)
    if endereco is None:
        continue
    try:
        usar(endereco)
    except grpc.RpcError as erro:
        # o nome está registrado, mas o servidor não respondeu
        # (por exemplo, encerrou sem fazer unbind)
        print("  %s não respondeu em %s (%s)" % (nome, endereco, erro.code().name))
