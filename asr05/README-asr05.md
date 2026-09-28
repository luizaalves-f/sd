# ASR05

Implementação da atividade ASR05 da disciplina de Sistemas Distribuídos.

## Funcionamento

O sistema é composto por cliente e servidor utilizando sockets TCP.

Foram implementadas três versões:

1. **Single-thread:** cliente e servidor processam as requisições sequencialmente.
2. **Multithread apenas no servidor:** o cliente envia requisições sequencialmente e o servidor cria uma nova thread para processar cada requisição.
3. **Multithread no cliente e no servidor:** cada requisição é enviada por uma nova thread no cliente e processada por uma nova thread no servidor.

As requisições são geradas automaticamente pelo cliente e utilizam as operações:

- transformar texto em maiúsculas;
- inverter texto;
- contar caracteres.

## Estrutura

```text
asr05/
├── single_thread/
├── server_multithread/
└── multithread/
```

Cada diretório contém um `cliente.py` e um `servidor.py`.

## Configuração

No cliente, o endereço do servidor é obtido de um arquivo `.env`:

```env
IP_DO_PEER01=IP_PRIVADO_DO_SERVIDOR
```

No servidor:

```python
HOST = "0.0.0.0"
PORT = 5000
```

## Como executar

Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
.venv\Scripts\activate
pip install python-dotenv
```

Em seguida, acesse a pasta da versão desejada.

Na máquina servidor:

```bash
python3 servidor.py
```

Na máquina cliente:

```bash
python3 cliente.py
```

## Experimento

O experimento foi realizado em duas instâncias EC2 distintas da AWS, uma utilizada como cliente e outra como servidor.

Foram enviadas **1000 requisições** em cada configuração.

|                  Versão               |   Tempo  | Requisições/s  |
| Single-thread                         | 0,4680 s |    2136,84     |
| Multithread apenas no servidor        | 0,6996 s |    1429,40     |
| Multithread no cliente e no servidor  | 0,4238 s |    2359,53     |

A versão multithread no cliente e no servidor apresentou o menor tempo de execução.

A versão com multithreading apenas no servidor apresentou desempenho inferior porque o cliente continuou enviando uma requisição por vez e aguardando a resposta antes de enviar a próxima. Dessa forma, houve o custo de criação das threads no servidor sem que a concorrência fosse plenamente aproveitada.

Já na versão totalmente multithread, múltiplas requisições puderam ser enviadas e processadas concorrentemente.