# Sistema de Mensageria do Banco Central

Este projeto foi desenvolvido para a disciplina de Sistemas Paralelos e Distribuídos.

O objetivo do projeto é simular um sistema de mensageria do Banco Central inspirado no funcionamento do PIX. Nesse sistema, bancos simulados geram transações e enviam essas mensagens para um broker RabbitMQ. Em seguida, um serviço de auditoria consome as mensagens e salva cada transação em um arquivo chamado `audit.log`.

## Integrantes

- Alexia Josielly Duarte da Silva Alves
- Maria Vitória Melo dos Santos

## Tecnologias Utilizadas

- Python
- RabbitMQ
- Docker
- Pika

## Estrutura do Projeto

```txt
sistema-mensageria-banco-central/
│
├── docker-compose.yml
├── requirements.txt
├── config.py
├── produtor_banco.py
├── servico_auditoria.py
├── README.md
└── .gitignore
```

## Funcionamento do Sistema

O sistema possui três partes principais:

1. Produtores, que representam os bancos simulados.
2. Message broker, responsável por receber e distribuir as mensagens.
3. Consumidor, representado pelo serviço de auditoria.

O fluxo funciona da seguinte forma:

```txt
banco_a  ─┐
banco_b  ─┼──> RabbitMQ ───> Serviço de Auditoria ───> audit.log
banco_c  ─┘
```

## Produtores

O arquivo `produtor_banco.py` representa um banco simulado.

Cada produtor gera transações PIX com informações como ID da transação, horário, banco de origem, banco de destino, contas e valor.

É possível executar vários bancos ao mesmo tempo, por exemplo:

```bash
py produtor_banco.py banco_a
```

```bash
py produtor_banco.py banco_b
```

```bash
py produtor_banco.py banco_c
```

## Message Broker

O RabbitMQ é utilizado como broker de mensagens.

Ele recebe as transações enviadas pelos bancos e entrega essas mensagens ao serviço consumidor.

O RabbitMQ é iniciado com Docker através do arquivo `docker-compose.yml`.

## Consumidor

O arquivo `servico_auditoria.py` representa o Audit Logging Service.

Esse serviço fica escutando a fila do RabbitMQ. Sempre que uma nova transação chega, ele extrai os dados principais e salva uma nova linha no arquivo `audit.log`.

## Formato da Mensagem

Cada transação gerada possui o seguinte formato:

```json
{
  "transactionId": "TX123456",
  "timestamp": "2026-06-01T10:15:30",
  "senderBank": "banco_a",
  "receiverBank": "banco_b",
  "senderAccount": "12345",
  "receiverAccount": "98765",
  "amount": 1500.50
}
```

## Formato do Arquivo audit.log

O serviço de auditoria salva as transações no seguinte formato:

```txt
[2026-06-20 11:55:25] TX5F9D6782 | banco_a | banco_c | 4552.76
[2026-06-20 11:55:28] TX3DA3A03B | banco_a | banco_d | 1919.74
[2026-06-20 11:55:31] TX975C2A09 | banco_a | banco_b | 2494.60
```

Cada nova transação é adicionada ao final do arquivo, sem apagar os registros anteriores.

## Como Executar o Projeto

Primeiro, instale as dependências:

```bash
pip install -r requirements.txt
```

Ou:

```bash
py -m pip install -r requirements.txt
```

Depois, suba o RabbitMQ com Docker:

```bash
docker compose up -d
```

O painel do RabbitMQ pode ser acessado em:

```txt
http://localhost:15672
```

Usuário:

```txt
guest
```

Senha:

```txt
guest
```

Em seguida, execute o serviço de auditoria:

```bash
py servico_auditoria.py
```

Em outros terminais, execute os bancos produtores:

```bash
py produtor_banco.py banco_a
```

```bash
py produtor_banco.py banco_b
```

```bash
py produtor_banco.py banco_c
```

## Resultado Esperado

Ao executar o sistema, os bancos simulados começam a gerar transações continuamente.

O serviço de auditoria consome essas mensagens pelo RabbitMQ e cria o arquivo `audit.log`, adicionando uma nova linha para cada transação recebida.

## Como Parar o Sistema

Para parar os produtores ou o serviço de auditoria, pressione:

```txt
Ctrl + C
```

Para parar o RabbitMQ, execute:

```bash
docker compose down
```

## Observação

O arquivo `audit.log` não é enviado para o repositório porque ele é gerado durante a execução do sistema.
