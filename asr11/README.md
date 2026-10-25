# ASR11

Implementação da atividade ASR11 da disciplina de Sistemas Distribuídos utilizando gRPC.

## Objetivo

Implementar dois serviços remotos em máquinas diferentes, um cliente que os acessa e um serviço de nomes (`bind`, `lookup`, `unbind` e `rebind`) para o cliente descobrir o endereço dos serviços, em gRPC.

## Estrutura

- `gRPC-SimpleNamingService/`: exemplo do professor, sem alterações
- `implementacao/`: minha implementação
  - `protos/`: interfaces `nomes.proto`, `calculadora.proto` e `texto.proto`
  - `python/`: servidores, cliente e configuração

## O que foi implementado

- **Serviço de nomes** (`servidor_nomes.py`): baseado no exemplo do professor. Toda resposta passa a ter status `OK` ou `NOK`, e os casos de erro (nome repetido no `bind`, nome inexistente no `lookup`, `unbind` ou `rebind`) são tratados.
- **Calculadora** (porta 5679): `Somar`, `Subtrair`, `Multiplicar` e `Dividir`.
- **Texto** (porta 5680): `Inverter`, `Maiusculas` e `ContarCaracteres`.
- **Cliente** (`cliente.py`): conhece só o endereço do serviço de nomes. Faz `lookup` de cada serviço e depois chama as operações.

Cada servidor faz `bind` ao iniciar (ou `rebind`, se o nome já existir) e `unbind` ao ser encerrado com `Ctrl+C`.

## Execução

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r implementacao/requirements.txt
cd implementacao
python3 -m grpc_tools.protoc -I protos --python_out=python --grpc_python_out=python protos/*.proto
cd python
export IP_NOMES=IP_PRIVADO_DO_SERVICO_DE_NOMES
```

Cada programa em um terminal:

```bash
python3 servidor_nomes.py
python3 servidor_calculadora.py
python3 servidor_texto.py
python3 cliente.py
```

## Resultado

Executado em duas instâncias EC2:

- instância 1 (172.31.87.73): serviço de nomes e Calculadora;
- instância 2 (172.31.81.247): Texto e cliente.

Saída do cliente:

```text
lookup de Calculadora: 172.31.87.73:5679
  Somar(10, 4) = 14
  Subtrair(10, 4) = 6
  Multiplicar(10, 4) = 40
  Dividir(10, 4) = 2.5
  Dividir(1, 0): erro, divisão por zero

lookup de Texto: 172.31.81.247:5680
  Inverter('Sistemas Distribuidos') = sodiubirtsiD sametsiS
  Maiusculas('Sistemas Distribuidos') = SISTEMAS DISTRIBUIDOS
  ContarCaracteres('Sistemas Distribuidos') = 21
```

Para testar o `rebind`, o Texto foi iniciado também na instância 1. Como o nome já existia, o endereço foi atualizado, e o cliente passou a encontrá-lo lá:

```text
rebind de Texto -> 172.31.87.73:5680: OK (endereço atualizado)
lookup de Texto: 172.31.87.73:5680
```

Trecho do log do serviço de nomes durante o teste (sem as linhas de `lookup`):

```text
Bind: Calculadora -> 172.31.87.73:5679
Bind: Texto -> 172.31.81.247:5680
Bind recusado: Texto já registrado
Rebind: Texto -> 172.31.87.73:5680
Unbind: Texto
Unbind: Calculadora
```

## Limitações

- Os registros ficam só na memória: se o serviço de nomes for reiniciado, eles se perdem.
- Se um servidor cair sem `Ctrl+C`, ele não faz `unbind`, e o cliente recebe um endereço desatualizado.
