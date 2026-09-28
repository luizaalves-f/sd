# ASR06

Implementação da atividade ASR06 da disciplina de Sistemas Distribuídos utilizando o middleware ZeroC Ice.

## Alterações realizadas

A interface `Printer.ice` foi estendida com dois novos métodos:

- `inverterString`: recebe uma string e retorna o texto invertido;
- `contarCaracteres`: recebe uma string e retorna a quantidade de caracteres.

A interface ficou definida da seguinte forma:

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

Os métodos foram implementados no servidor e chamados remotamente pelos clientes.

## Execução

O experimento foi realizado utilizando duas instâncias EC2 distintas:

- uma instância como servidor;
- uma instância como cliente.

O Ice e o compilador `slice2py` foram instalados nas duas máquinas.

A interface foi compilada em ambas com:

```bash
slice2py Printer.ice
```

No servidor:

```bash
python3 server2.py
```

No cliente:

```bash
python3 client2.py
```

O cliente utiliza o endereço do servidor configurado em um arquivo `.env`:

```env
IP_SERVIDOR=IP_PRIVADO_DO_SERVIDOR
```

## Resultado

As chamadas remotas foram executadas com sucesso para os dois objetos do servidor.

Exemplo de saída no cliente:

```text
Hello World from printer1!*
String invertida: sodiubirtsiD sametsiS
Quantidade de caracteres: 21

Hello World from printer2!*
String invertida: ecI erawelddiM
Quantidade de caracteres: 14
```

O servidor também registrou o processamento das chamadas remotas realizadas pelos dois objetos.