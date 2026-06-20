# produtor_banco.py

import json
import random
import sys
import time
import uuid
from datetime import datetime

import pika

from config import RABBITMQ_HOST, NOME_FILA, BANCOS


def conectar_rabbitmq():
    # aqui eu conecto no rabbitmq que está rodando no computador
    conexao = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    # aqui eu crio um canal de comunicação com o rabbitmq
    canal = conexao.channel()

    # aqui eu crio a fila se ela ainda não existir
    canal.queue_declare(queue=NOME_FILA, durable=True)

    return conexao, canal


def criar_transacao(nome_banco):
    # aqui eu pego todos os bancos menos o banco que está enviando
    bancos_destino = [banco for banco in BANCOS if banco != nome_banco]

    # aqui eu escolho um banco aleatório pra receber a transação
    banco_destino = random.choice(bancos_destino)

    # aqui eu monto uma transação pix falsa
    transacao = {
        "transactionId": "TX" + str(uuid.uuid4())[:8].upper(),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "senderBank": nome_banco,
        "receiverBank": banco_destino,
        "senderAccount": str(random.randint(10000, 99999)),
        "receiverAccount": str(random.randint(10000, 99999)),
        "amount": round(random.uniform(10, 5000), 2)
    }

    return transacao


def enviar_transacao(canal, transacao):
    # aqui eu transformo a transação em texto json
    mensagem = json.dumps(transacao)

    # aqui eu envio a mensagem para a fila do rabbitmq
    canal.basic_publish(
        exchange="",
        routing_key=NOME_FILA,
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
            content_type="application/json"
        )
    )

    print(f"transação enviada: {mensagem}")


def main():
    # aqui eu pego o nome do banco pelo terminal
    # exemplo: python produtor_banco.py banco_a
    if len(sys.argv) > 1:
        nome_banco = sys.argv[1]
    else:
        nome_banco = "banco_a"

    # aqui eu verifico se o banco existe na lista do config.py
    if nome_banco not in BANCOS:
        print("banco inválido")
        print(f"bancos disponíveis: {BANCOS}")
        return

    conexao, canal = conectar_rabbitmq()

    print(f"{nome_banco} iniciado")
    print("enviando transações pix para o banco central...")

    try:
        while True:
            # aqui eu crio uma nova transação
            transacao = criar_transacao(nome_banco)

            # aqui eu envio essa transação para o rabbitmq
            enviar_transacao(canal, transacao)

            # aqui eu espero de 1 a 5 segundos antes de enviar outra
            time.sleep(random.randint(1, 5))

    except KeyboardInterrupt:
        print("\nprodutor encerrado")

    finally:
        conexao.close()


if __name__ == "__main__":
    main()