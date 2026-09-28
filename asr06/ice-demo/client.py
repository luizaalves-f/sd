import sys, Ice
import Demo
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("IP_SERVIDOR")
 
communicator = Ice.initialize(sys.argv)

base = communicator.stringToProxy("SimplePrinter:tcp -h {HOST} -p 5678")
printer = Demo.PrinterPrx.checkedCast(base)
if not printer:
    raise RuntimeError("Invalid proxy")

rep = printer.printString("Hello World!")
print("Resposta printString:", rep)

rep = printer.inverterString("Sistemas Distribuidos")
print("String invertida:", rep)

rep = printer.contarCaracteres("Sistemas Distribuidos")
print("Quantidade de caracteres:", rep)