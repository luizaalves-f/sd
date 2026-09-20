# ASR04

Implementação da atividade ASR04 da disciplina de Sistemas Digitais.

A aplicação utiliza sockets TCP para comunicação entre cliente e servidor. O cliente pode solicitar diferentes operações, que são processadas pelo servidor.

## Como executar

No terminal, acesse o diretório `sd/asr04` e crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Em seguida, execute o servidor:

```powershell
python servidor.py
```

Em outro terminal, acesse novamente o diretório `sd/asr04`, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

E execute o cliente:

```powershell
python cliente.py
```

## Funcionamento

A aplicação implementa uma comunicação cliente-servidor utilizando sockets TCP.

O servidor fica aguardando a conexão de um cliente e, após a conexão ser estabelecida, recebe requisições contendo uma operação e um texto.

O cliente pode solicitar diferentes funcionalidades ao servidor:

- transformar o texto em letras maiúsculas
- inverter o texto
- contar a quantidade de caracteres

A requisição é enviada no formato:

```text
operacao|texto
```

Por exemplo:

```text
1|sistemas distribuídos
```

Nesse caso, o servidor identifica a operação `1`, transforma o texto em letras maiúsculas e retorna:

```text
SISTEMAS DISTRIBUÍDOS
```

A conexão permanece aberta para que o cliente possa realizar várias requisições antes de encerrar a comunicação.