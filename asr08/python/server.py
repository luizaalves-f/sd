import sys
import Ice
import Demo


class PrinterI(Demo.Printer):
    def printString(self, s, current=None):
        print("printString:", s)
        return s + "*"

    def inverterString(self, s, current=None):
        resultado = s[::-1]
        print("inverterString:", resultado)
        return resultado

    def contarCaracteres(self, s, current=None):
        quantidade = len(s)
        print("contarCaracteres:", quantidade)
        return quantidade


communicator = Ice.initialize(sys.argv)

adapter = communicator.createObjectAdapterWithEndpoints(
    "SimpleAdapter",
    "tcp -p 5678"
)

printer = PrinterI()

adapter.add(
    printer,
    Ice.Identity("SimplePrinter")
)

adapter.activate()

print("Servidor Python aguardando requisições na porta 5678...")

communicator.waitForShutdown()