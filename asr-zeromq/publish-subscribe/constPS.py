import os

# IP do publisher (usado pelos subscribers). Pode ser trocado sem editar o código:
#   export IP_PUBLISHER=172.31.x.x
HOST = os.getenv("IP_PUBLISHER", "127.0.0.1")
PORT = "4567"

LIMITE_ALERTA = 30.0    # temperatura (°C) a partir da qual sai um ALERTA
