import sys
import os
import Ice
import Demo
from dotenv import load_dotenv


load_dotenv()

HOST = os.getenv("IP_SERVIDOR")

communicator = Ice.initialize(sys.argv)

base = communicator.stringToProxy(
    f"SimplePrinter:tcp -h {HOST} -p 5678"
)

printer = Demo.PrinterPrx.checkedCast(base)

if not printer:
    raise RuntimeError("Invalid proxy")

rep = printer.printString("Hello from Python client!")
print("Resposta printString:", rep)

rep = printer.inverterString("Sistemas Distribuidos")
print("String invertida:", rep)

rep = printer.contarCaracteres("Sistemas Distribuidos")
print("Quantidade de caracteres:", rep)

communicator.destroy()