# ASR08

Implementação da atividade ASR08 da disciplina de Sistemas Distribuídos utilizando o middleware ZeroC Ice.

## Objetivo

Implementar dois cenários multiplataforma utilizando a mesma interface Slice:

1. Cliente em Python e servidor em Java.
2. Cliente em Java e servidor em Python.

## Interface remota

A interface utilizada foi definida em `Printer.ice`:

```ice
module Demo
{
    interface Printer
    {
        string printString(string s);
        string inverterString(string s);
        int contarCaracteres(string s);
    }
}
```

## Estrutura

```text
asr08/
├── Printer.ice
├── python/
│   ├── client.py
│   └── server.py
└── java/
    ├── build.gradle
    ├── settings.gradle
    └── src/
        └── main/
            ├── java/
            │   ├── Client.java
            │   └── Server.java
            └── slice/
                └── Printer.ice
```

## Cenário 1 — Cliente Python e servidor Java

No servidor Java:

```bash
gradle --no-daemon runServer
```

No cliente Python:

```bash
slice2py ../Printer.ice
python3 client.py
```

Resultado obtido no cliente:

```text
Resposta printString: Hello from Python client!*
String invertida: sodiubirtsiD sametsiS
Quantidade de caracteres: 21
```

## Cenário 2 — Cliente Java e servidor Python

No servidor Python:

```bash
slice2py ../Printer.ice
python3 server.py
```

No cliente Java:

```bash
gradle --no-daemon runClient --args="IP_DO_SERVIDOR"
```

Resultado obtido no cliente:

```text
Resposta printString: Hello from Java client!*
String invertida: sodiubirtsiD sametsiS
Quantidade de caracteres: 21
```

Os dois cenários foram executados com sucesso em instâncias EC2 distintas.
