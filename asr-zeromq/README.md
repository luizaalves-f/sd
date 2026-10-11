# ASR ZeroMQ

Implementação da atividade da disciplina de Sistemas Distribuídos utilizando o middleware ZeroMQ.

## Objetivo

Testar em máquinas diferentes os exemplos das Figs. 4.21, 4.22 e 4.23 e acrescentar novas funcionalidades a cada um deles:

1. Request-reply (`request-reply/`)
2. Publish-subscribe (`publish-subscribe/`)
3. Pipeline (`pipeline/`)

A pasta `outros-exemplos/` contém os exemplos de RPC que vieram no mesmo pacote, mas que não fazem parte desta atividade.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install pyzmq
```

## Configuração

Os processos que fazem `bind` escutam em todas as interfaces. Os que fazem `connect` leem o IP de uma variável de ambiente (se ela não existir, é usado `127.0.0.1`):

```bash
export IP_SERVIDOR=IP_PRIVADO      # request-reply
export IP_PUBLISHER=IP_PRIVADO     # publish-subscribe
export IP_SRC1=IP_PRIVADO          # pipeline
export IP_SRC2=IP_PRIVADO
export IP_SINK=IP_PRIVADO
```

As portas usadas são 5678, 5679 e 5680.

## 1. Request-reply

### Alterações realizadas

- O servidor passou a aceitar comandos: `ECHO`, `UPPER`, `REVERSE`, `COUNT`, `TIME`, `STATS` e `STOP`. O `ECHO` mantém o comportamento original (devolve a mensagem com `*`) e o `STATS` mostra quantas requisições o servidor já atendeu.
- O cliente espera a resposta por 2,5 segundos e tenta até 3 vezes. No original, ele ficava bloqueado se o servidor não estivesse rodando.
- Os arquivos `client1.py` e `client2.py` foram substituídos pela opção `--porta` do `client.py`.

### Execução

No servidor:

```bash
python3 server.py
```

No cliente:

```bash
python3 client.py
python3 client.py --porta 2
python3 client.py UPPER ola mundo
python3 client.py STOP
```

### Resultado

Saída do cliente, com o servidor em outra instância:

```text
Conectado a tcp://172.31.87.73:5678
ECHO Hello world 1 -> Hello world 1*
UPPER sistemas distribuidos -> SISTEMAS DISTRIBUIDOS
REVERSE Sistemas Distribuidos -> sodiubirtsiD sametsiS
COUNT Sistemas Distribuidos -> 21
TIME -> Sun Oct 11 15:39:35 2026
STATS -> 6 requisicoes em 7s (COUNT=1, ECHO=1, REVERSE=1, STATS=1, TIME=1, UPPER=1)
Conectado a tcp://172.31.87.73:5679
ECHO Hello world 2 -> Hello world 2*
UPPER sistemas distribuidos -> SISTEMAS DISTRIBUIDOS
REVERSE Sistemas Distribuidos -> sodiubirtsiD sametsiS
COUNT Sistemas Distribuidos -> 21
TIME -> Sun Oct 11 15:39:35 2026
STATS -> 12 requisicoes em 7s (COUNT=2, ECHO=2, REVERSE=2, STATS=2, TIME=2, UPPER=2)
Conectado a tcp://172.31.87.73:5678
STOP -> Servidor encerrado
```

Com o servidor desligado (teste feito localmente):

```text
Conectado a tcp://127.0.0.1:5678
  sem resposta (tentativa 1 de 3)
  sem resposta (tentativa 2 de 3)
  sem resposta (tentativa 3 de 3)
Servidor indisponível, desistindo.
```

## 2. Publish-subscribe

### Alterações realizadas

- O publisher publica quatro tópicos: `TIME`, `TEMP` e `UMID` a cada segundo (temperatura e umidade são simuladas) e `ALERTA` quando a temperatura passa de 30 °C.
- O subscriber escolhe os tópicos e a quantidade de mensagens pela linha de comando.
- As mensagens têm um número de sequência por tópico, que o subscriber usa para avisar quando alguma mensagem foi perdida.

### Execução

No publisher:

```bash
python3 publisher.py
```

No subscriber:

```bash
python3 subscriber.py
python3 subscriber.py TEMP ALERTA -n 10
```

### Resultado

Saída do subscriber, com o publisher em outra instância:

```text
Assinando TEMP, ALERTA em tcp://172.31.87.73:5678
[TEMP #20] 28.7
[TEMP #21] 28.7
[TEMP #22] 28.3
[TEMP #23] 28.3
[TEMP #24] 28.0
[TEMP #25] 28.7
[TEMP #26] 29.9
[TEMP #27] 30.2
[ALERTA #7] temperatura alta: 30.2 C
[TEMP #28] 29.4
Recebidas: 10 | perdidas detectadas: 0
  ALERTA: última mensagem foi a #7
  TEMP: última mensagem foi a #28
```

A primeira mensagem recebida é a #20 porque as anteriores foram publicadas antes de o subscriber se conectar.

## 3. Pipeline

### Alterações realizadas

- Foi criado o `sink.py`, que recebe os resultados dos workers e mostra um resumo de quantas tarefas cada worker executou.
- O worker verifica se a carga recebida é um número primo e envia o resultado para o sink.
- A quantidade de tarefas e o intervalo entre elas podem ser passados como argumento para o `tasksrc.py`.

### Execução

```bash
python3 sink.py
python3 taskwork.py w1
python3 taskwork.py w2
python3 tasksrc.py 1 20
python3 tasksrc.py 2 20
```

Os workers precisam ser iniciados antes das fontes.

### Resultado

Saída do sink (final), com 20 tarefas de cada fonte:

```text
w1 concluiu tarefa 15 da fonte 2 (carga 70) em 0.70s
w2 concluiu tarefa 16 da fonte 2 (carga 62) em 0.62s
w1 concluiu tarefa 17 da fonte 2 (carga 10) em 0.10s
w2 concluiu tarefa 18 da fonte 2 (carga 63) em 0.63s
w1 concluiu tarefa 19 da fonte 2 (carga 16) em 0.16s
w2 concluiu tarefa 20 da fonte 2 (carga 95) em 0.95s

===== Resumo: 40 tarefas concluidas =====
  worker w1        25 tarefas ( 62.5%) | carga total 1420 | 14.20s trabalhando
  worker w2        15 tarefas ( 37.5%) | carga total  914 | 9.14s trabalhando
  fonte 1: 20 tarefas
  fonte 2: 20 tarefas
  cargas primas encontradas: 6 [3, 7, 37, 59, 73, 89]
```

Com os dois workers conectados, as tarefas de cada fonte são entregues alternadamente a eles.

## Execução na AWS

Os três exemplos foram executados em duas instâncias EC2 distintas, usando os IPs privados:

| Exemplo           | Instância 1 (172.31.87.73)        | Instância 2 (172.31.81.247) |
|-------------------|-----------------------------------|-----------------------------|
| Request-reply     | servidor                          | cliente                     |
| Publish-subscribe | publisher                         | subscriber                  |
| Pipeline          | sink, worker `w1` e fonte 1       | worker `w2` e fonte 2       |
