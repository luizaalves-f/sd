import sys, Ice
import Demo
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("IP_SERVIDOR")
 
communicator = Ice.initialize(sys.argv)

base1 = communicator.stringToProxy(f"SimplePrinter1:tcp -h {HOST} -p 5678")
base2 = communicator.stringToProxy(f"SimplePrinter2:tcp -h {HOST} -p 5678")
printer1 = Demo.PrinterPrx.checkedCast(base1)
printer2 = Demo.PrinterPrx.checkedCast(base2)
if (not printer1) or (not printer2):
    raise RuntimeError("Invalid proxy")

rep = printer1.printString("Hello World from printer1!")
print(rep)

rep = printer1.inverterString("Sistemas Distribuidos")
print("String invertida:", rep)

rep = printer1.contarCaracteres("Sistemas Distribuidos")
print("Quantidade de caracteres:", rep)

rep = printer2.printString("Hello World from printer2!")
print(rep)

rep = printer2.inverterString("Middleware Ice")
print("String invertida:", rep)

rep = printer2.contarCaracteres("Middleware Ice")
print("Quantidade de caracteres:", rep)

communicator.waitForShutdown()
