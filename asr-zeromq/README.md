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

```text
Conectado a tcp://127.0.0.1:5678
ECHO Hello world 1 -> Hello world 1*
UPPER sistemas distribuidos -> SISTEMAS DISTRIBUIDOS
REVERSE Sistemas Distribuidos -> sodiubirtsiD sametsiS
COUNT Sistemas Distribuidos -> 21
TIME -> Sun Oct 11 11:50:30 2026
STATS -> 6 requisicoes em 1s (COUNT=1, ECHO=1, REVERSE=1, STATS=1, TIME=1, UPPER=1)
```

Com o servidor desligado:

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

```text
Assinando TEMP, ALERTA em tcp://127.0.0.1:5678
[TEMP #2] 28.3
[TEMP #3] 27.3
[TEMP #4] 26.4
[TEMP #5] 26.6
Recebidas: 4 | perdidas detectadas: 0
  TEMP: última mensagem foi a #5
```

A primeira mensagem recebida é a #2 porque a #1 foi publicada antes de o subscriber se conectar.

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
python3 tasksrc.py 1 10 0.2
python3 tasksrc.py 2 10 0.2
```

Os workers precisam ser iniciados antes das fontes.

### Resultado

Saída do sink:

```text
w1 concluiu tarefa 8 da fonte 2 (carga 83, primo) em 0.83s
w1 concluiu tarefa 10 da fonte 2 (carga 65) em 0.65s

===== Resumo: 20 tarefas concluidas =====
  worker w1        12 tarefas ( 60.0%) | carga total  598 | 5.99s trabalhando
  worker w2         8 tarefas ( 40.0%) | carga total  301 | 3.01s trabalhando
  fonte 1: 10 tarefas
  fonte 2: 10 tarefas
  cargas primas encontradas: 8 [3, 11, 23, 29, 41, 71, 79, 83]
```

<!-- TODO: as saídas acima são do teste local. Depois de rodar nas instâncias EC2,
     trocar pelas saídas da AWS e dizer aqui o que rodou em cada instância. -->
