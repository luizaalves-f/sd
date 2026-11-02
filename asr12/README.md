# ASR12

Comparaçao entre RESTful e gRPC, feita a partir de duas implementaçoes do mesmo serviço de cadastro de funcionarios

## Estrutura

- `RESTful-WS-Example/`: exemplo do professor com RESTful (Flask), sem alteraçoes
- `gRPC-WS-Example/`: o mesmo exemplo com gRPC, sem alteraçoes
- `medicao/`: script que mede o tamanho das mensagens e o tempo de resposta dos dois exemplos

Os dois servidores guardam uma lista de funcionarios em memoria e permitem criar, consultar, listar, atualizar e remover funcionarios. Eles nao sao exatamente equivalentes: so o RESTful tem salario, e o id e texto no RESTful e numero no gRPC

## 1. Modelo de programaçao

**RESTful** e organizado em **recursos** identificados por URLs, e as operaçoes sao sempre os mesmos metodos HTTP (`GET`, `POST`, `PUT`, `DELETE`). Nao existe um arquivo que defina a interface: o contrato sao as URLs, os campos do JSON e a documentaçao. O cliente monta tudo manualmente:

```python
response = requests.put(api_base_url + '/101', json={"title": "Programmer"})
```

**gRPC** e uma chamada de procedimento remoto: as operaçoes especificas da aplicaçao e os tipos das mensagens sao declarados no arquivo `.proto`, e o `protoc` gera o stub do cliente e a base do servidor. O cliente chama o stub como se fosse um objeto local:

```python
response = stub.UpdateEmployeeTitle(EmployeeService_pb2.EmployeeTitleUpdate(id=301, title='Senior Programmer'))
```

Ou seja, no RESTful a interface e **generica** (os mesmos metodos para todos os recursos) e no gRPC e **especifica** (cada operaçao tem nome, parametros e retorno proprios). O proprio exemplo RESTful mostra o risco de depender de convençoes: a atualizaçao de salario coloca o valor na URL (`PUT /empdb/employee/101/4000`), o que foge do estilo REST

## 2. Eficiencia

Medido com `medicao/medicao.py`, que executa os dois servidores do professor e faz as mesmas operaçoes nos dois:

| | RESTful (JSON) | gRPC (Protocol Buffers) |
|---|---|---|
| Tamanho: consultar 1 funcionario | 95 bytes | 33 bytes |
| Tamanho: listar 1000 funcionarios | 62.062 bytes | 36.002 bytes |
| Tempo: consultar 1 funcionario | 5,4 a 8,5 ms | 1,5 a 2,6 ms |
| Tempo: listar 1000 funcionarios | 12,8 a 14,6 ms | 8,9 a 9,0 ms |

Os tempos sao a mediana de 1000 requisiçoes, em tres execuçoes. O gRPC foi mais eficiente em todos os casos porque usa formato binario, que nao repete os nomes dos campos em cada registro, e HTTP/2, que comprime os cabeçalhos. O RESTful ainda envia cerca de 306 bytes de cabeçalhos HTTP/1.1 por requisiçao

Ressalva: a mediçao foi feita em uma unica maquina, com o servidor de desenvolvimento do Flask, e os tempos variaram entre execuçoes. Os valores servem como referencia; o que se manteve foi o gRPC ser mais rapido

## 3. Modularidade

No gRPC, a interface fica separada da implementaçao, no `.proto`: o servidor pode ser reescrito, ate em outra linguagem, sem mudar o cliente. No RESTful, essa separaçao e informal, mas os recursos sao faceis de dividir entre serviços, e proxies e caches HTTP funcionam sem conhecer o serviço

## 4. Manutenibilidade

- **Erros de tipo:** no gRPC, um id negativo ou com texto foi rejeitado pelo proprio cliente, antes de enviar. No RESTful, um `POST` sem o campo `name` so deu erro no servidor (HTTP 500), e o `salary` enviado pelo cliente foi descartado sem aviso
- **Evoluçao:** no gRPC, cada campo tem um numero fixo, entao da para acrescentar campos sem quebrar clientes antigos. No RESTful, nada avisa o cliente quando um campo muda; e comum usar versoes na URL e documentar com OpenAPI
- **Tratamento de erros:** nenhum dos exemplos usa os codigos de erro da propria tecnologia. Um id inexistente devolve HTTP 200 com lista vazia no RESTful e uma exceçao generica (`UNKNOWN`) no gRPC, quando deveriam ser 404 e `NOT_FOUND`

## 5. Abertura

O RESTful e mais aberto: usa HTTP e JSON, e respondeu normalmente a requisiçoes feitas com `curl`. O gRPC tambem e um padrao aberto e funciona em varias linguagens, mas exige o `.proto` e uma biblioteca gRPC; o `curl` nao conseguiu se comunicar com ele

## 6. Transparencia de distribuiçao

O gRPC tem mais **transparencia de acesso**: a chamada remota parece uma chamada local, enquanto o cliente RESTful lida com URLs, metodos HTTP e JSON. Mas nao e transparencia total, porque falhas de rede aparecem como exceçoes `RpcError`

Nenhum dos dois tem **transparencia de localizaçao**: o IP e a porta do servidor estao fixos no `const.py`. Um serviço de nomes, como o da ASR11, resolveria isso

## Resumo

| Aspecto | RESTful | gRPC |
|---|---|---|
| Modelo de programaçao | Recursos e metodos HTTP genericos | Procedimentos remotos especificos |
| Interface | Implicita (URLs e documentaçao) | Explicita e tipada (`.proto`) |
| Eficiencia | Menor (texto, HTTP/1.1) | Maior (binario, HTTP/2) |
| Erros de tipo | Detectados so no servidor | Detectados antes de enviar |
| Abertura | Maior | Menor |
| Transparencia de acesso | Menor | Maior |

## 7. Comparaçao mais ampla

### APIs para o frontend

Para aplicaçoes de usuario final, principalmente as que rodam no navegador, o RESTful costuma ser a melhor escolha:

- **Navegador:** o JavaScript faz requisiçoes HTTP e le JSON sem nenhuma biblioteca extra. O gRPC nao pode ser chamado diretamente pelo navegador, porque o navegador nao da acesso aos detalhes do HTTP/2 que o gRPC usa. E preciso usar o gRPC-Web com um proxy no meio, e ele nao suporta todos os tipos de chamada (por exemplo, streaming do cliente para o servidor)
- **APIs publicas:** quem vai usar a API pode testa-la com `curl` ou pelo navegador, sem precisar do `.proto` nem gerar codigo
- **Cache:** respostas de `GET` podem ser guardadas por caches e CDNs comuns. O gRPC envia tudo como `POST`, entao esses caches nao funcionam com ele

Em aplicativos moveis, o gRPC e uma opçao viavel, porque existem bibliotecas para Android e iOS, e mensagens menores economizam dados e bateria

### APIs entre serviços (backend)

Na comunicaçao entre serviços, principalmente em arquiteturas de microsserviços, o gRPC tem vantagens:

- **Desempenho:** sao muitas chamadas internas, e a diferença de tamanho e tempo medida na seçao 2 se acumula
- **Contrato:** o `.proto` compartilhado garante que serviços escritos por equipes e linguagens diferentes concordem sobre a interface, e o codigo e gerado automaticamente
- **Recursos prontos:** streaming nos dois sentidos, prazos (deadlines) que se propagam entre serviços e cancelamento de chamadas
- **Ambiente controlado:** como os dois lados sao do mesmo sistema, a menor abertura do gRPC nao e um problema

O RESTful continua comum no backend quando a simplicidade importa mais que o desempenho, ou na integraçao com sistemas externos. Um padrao frequente e usar RESTful na borda, para os clientes externos, e gRPC entre os serviços internos

### Fatores a considerar na escolha

| Fator | Favorece RESTful | Favorece gRPC |
|---|---|---|
| Quem consome a API | Navegador, terceiros, API publica | Serviços internos do mesmo sistema |
| Desempenho e volume de chamadas | Volume baixo ou moderado | Muitas chamadas, baixa latencia |
| Streaming | Nao e necessario | Necessario (dados continuos, nos dois sentidos) |
| Contrato e tipos | Flexibilidade, poucos clientes | Varias linguagens e equipes, contrato rigido |
| Infraestrutura | Proxies, caches e balanceadores HTTP comuns | Infraestrutura com suporte a HTTP/2 |
| Depuraçao | Mensagens legiveis (JSON) | Aceita mensagens binarias e ferramentas especificas |
| Equipe | Familiaridade com HTTP e JSON | Familiaridade com IDL e geraçao de codigo |

Sobre a infraestrutura: como o gRPC mantem uma conexao HTTP/2 aberta por muito tempo, um balanceador que so distribui conexoes manda todas as chamadas de um cliente para o mesmo servidor. E preciso um balanceador que entenda HTTP/2 e distribua cada chamada

### Conclusao

Nenhuma das duas tecnologias e melhor em todos os casos. O RESTful prioriza **abertura e simplicidade**, o que o torna adequado para APIs consumidas por navegadores e por terceiros. O gRPC prioriza **eficiencia e contrato rigido**, o que o torna adequado para a comunicaçao entre serviços de um mesmo sistema. A escolha depende principalmente de quem vai consumir a API e de quanto o desempenho importa
