import sys

import texto_pb2
import texto_pb2_grpc

import config
import registro


class Texto(texto_pb2_grpc.TextoServicer):

    def Inverter(self, request, context):
        print("Inverter('%s')" % request.texto)
        return texto_pb2.TextoMsg(texto=request.texto[::-1])

    def Maiusculas(self, request, context):
        print("Maiusculas('%s')" % request.texto)
        return texto_pb2.TextoMsg(texto=request.texto.upper())

    def ContarCaracteres(self, request, context):
        print("ContarCaracteres('%s')" % request.texto)
        return texto_pb2.ContagemMsg(quantidade=len(request.texto))


if __name__ == "__main__":
    # a porta pode ser trocada pelo primeiro argumento: python servidor_texto.py 5681
    porta = sys.argv[1] if len(sys.argv) > 1 else config.PORTA_TEXTO
    registro.executar_servidor(
        config.NOME_TEXTO, porta,
        lambda server: texto_pb2_grpc.add_TextoServicer_to_server(Texto(), server))
