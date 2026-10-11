import os

# IPs das máquinas que fazem bind (fontes e sink). Os workers se conectam a elas.
# Podem ser trocados sem editar o código:
#   export IP_SRC1=172.31.x.x IP_SRC2=172.31.y.y IP_SINK=172.31.z.z
SRC1  = os.getenv("IP_SRC1", "127.0.0.1")
SRC2  = os.getenv("IP_SRC2", "127.0.0.1")
SINK  = os.getenv("IP_SINK", "127.0.0.1")
PORT1 = "5678"   # task source 1
PORT2 = "5679"   # task source 2
PORT3 = "5680"   # sink
