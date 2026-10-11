import os

# IP do servidor (usado pelo cliente). Pode ser trocado sem editar o código:
#   export IP_SERVIDOR=172.31.x.x
HOST  = os.getenv("IP_SERVIDOR", "127.0.0.1")
PORT1 = "4567"
PORT2 = "4568"

TIMEOUT_MS = 2500   # tempo máximo de espera do cliente por uma resposta
TENTATIVAS = 3      # quantas vezes o cliente reenvia antes de desistir
