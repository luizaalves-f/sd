import sys

import calculadora_pb2
import calculadora_pb2_grpc

import config
import registro


class Calculadora(calculadora_pb2_grpc.CalculadoraServicer):

    def responder(self, operacao, request, valor):
        print("%s(%g, %g) = %g" % (operacao, request.a, request.b, valor))
        return calculadora_pb2.ResultadoMsg(status="OK", mensagem="", valor=valor)

    def Somar(self, request, context):
        return self.responder("Somar", request, request.a + request.b)

    def Subtrair(self, request, context):
        return self.responder("Subtrair", request, request.a - request.b)

    def Multiplicar(self, request, context):
        return self.responder("Multiplicar", request, request.a * request.b)

    def Dividir(self, request, context):
        if request.b == 0:
            print("Dividir(%g, 0) recusado" % request.a)
            return calculadora_pb2.ResultadoMsg(status="NOK", mensagem="divisão por zero")
        return self.responder("Dividir", request, request.a / request.b)


if __name__ == "__main__":
    # a porta pode ser trocada pelo primeiro argumento: python servidor_calculadora.py 5681
    porta = sys.argv[1] if len(sys.argv) > 1 else config.PORTA_CALCULADORA
    registro.executar_servidor(
        config.NOME_CALCULADORA, porta,
        lambda server: calculadora_pb2_grpc.add_CalculadoraServicer_to_server(Calculadora(), server))
