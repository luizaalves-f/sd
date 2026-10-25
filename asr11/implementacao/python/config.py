import os

# Endereço do serviço de nomes. Pode ser trocado sem editar o código:
#   export IP_NOMES=172.31.x.x
IP_NOMES    = os.getenv("IP_NOMES", "127.0.0.1")
PORTA_NOMES = os.getenv("PORTA_NOMES", "5678")

# Nomes e portas padrão dos serviços de aplicação
NOME_CALCULADORA  = "Calculadora"
PORTA_CALCULADORA = "5679"
NOME_TEXTO        = "Texto"
PORTA_TEXTO       = "5680"

# IP que os servidores registram no serviço de nomes. Se não for definido,
# é descoberto automaticamente (o IP da interface que alcança o serviço de nomes).
IP_PROPRIO = os.getenv("IP_PROPRIO")

TIMEOUT = 5   # segundos de espera por uma resposta do serviço de nomes
