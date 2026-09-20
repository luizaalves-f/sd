from socket import *

HOST = "127.0.0.1"
PORT = 5000

# Cria um socket TCP
s = socket(AF_INET, SOCK_STREAM)

# Conecta ao servidor
s.connect((HOST, PORT))

# Mantém o cliente ativo para permitir várias requisições
while True:
    print("\nFuncionalidades disponíveis:")
    print("1 - Transformar texto em maiúsculas")
    print("2 - Inverter texto")
    print("3 - Contar caracteres")
    print("0 - Sair")

    operacao = input("\nEscolha uma opção: ")

    # Encerra a comunicação com o servidor
    if operacao == "0":
        s.send("SAIR".encode())
        break

    texto = input("Digite o texto: ")

    # Monta a requisição no formato: operacao|texto
    requisicao = operacao + "|" + texto

    # Envia a requisição ao servidor
    s.send(requisicao.encode())

    # Aguarda e recebe a resposta do servidor
    data = s.recv(1024)

    print("Resposta do servidor:", data.decode())

# Fecha o socket após o encerramento
s.close()