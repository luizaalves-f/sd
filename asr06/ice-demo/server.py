import sys, Ice
import Demo
 
class PrinterI(Demo.Printer):
    def printString(self, s, current=None):
        print(s)
        return s + "*"

    def inverterString(self, s, current=None):
        resultado = s[::-1]
        print("String invertida:", resultado)
        return resultado

    def contarCaracteres(self, s, current=None):
        quantidade = len(s)
        print("Quantidade de caracteres:", quantidade)
        return quantidade

communicator = Ice.initialize(sys.argv) 

adapter = communicator.createObjectAdapterWithEndpoints("SimpleAdapter", "default -p 5678")
obj = PrinterI()
adapter.add(obj, Ice.Identity("SimplePrinter"))
adapter.activate()

communicator.waitForShutdown()
