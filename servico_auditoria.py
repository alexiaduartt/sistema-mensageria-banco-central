# servico_auditoria.py

import json

import pika

from config import RABBITMQ_HOST, NOME_FILA, ARQUIVO_LOG


def conectar_rabbitmq():
    # aqui eu conecto no rabbitmq
    conexao = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    # aqui eu crio um canal de comunicação
    canal = conexao.channel()

    # aqui eu garanto que a fila existe
    canal.queue_declare(queue=NOME_FILA, durable=True)

    # aqui eu faço o serviço pegar uma mensagem por vez
    canal.basic_qos(prefetch_count=1)

    return conexao, canal


def salvar_no_log(transacao):
    # aqui eu pego os dados principais da transação
    horario = transacao["timestamp"].replace("T", " ")
    id_transacao = transacao["transactionId"]
    banco_origem = transacao["senderBank"]
    banco_destino = transacao["receiverBank"]
    valor = transacao["amount"]

    # aqui eu monto a linha no formato parecido com o que o professor pediu
    linha_log = f"[{horario}] {id_transacao} | {banco_origem} | {banco_destino} | {valor:.2f}\n"

    # aqui eu abro o arquivo em modo "a"
    # esse modo adiciona no final do arquivo sem apagar o que já tinha
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha_log)

    return linha_log


def processar_mensagem(canal, metodo, propriedades, corpo):
    # aqui eu transformo a mensagem recebida em dicionário python
    transacao = json.loads(corpo.decode())

    # aqui eu salvo a transação no arquivo audit.log
    linha_log = salvar_no_log(transacao)

    print("transação salva no audit.log:")
    print(linha_log.strip())

    # aqui eu aviso ao rabbitmq que a mensagem foi processada
    canal.basic_ack(delivery_tag=metodo.delivery_tag)


def main():
    conexao, canal = conectar_rabbitmq()

    # aqui eu digo qual fila esse serviço vai escutar
    canal.basic_consume(
        queue=NOME_FILA,
        on_message_callback=processar_mensagem
    )

    print("serviço de auditoria iniciado")
    print("aguardando transações pix...")

    try:
        canal.start_consuming()

    except KeyboardInterrupt:
        print("\nserviço de auditoria encerrado")

    finally:
        conexao.close()


if __name__ == "__main__":
    main()