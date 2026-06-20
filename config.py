# config.py

# aqui fica o endereço do rabbitmq
RABBITMQ_HOST = "localhost"

# aqui fica o nome da fila onde as transações pix vão passar
NOME_FILA = "pix_transacoes"

# aqui fica o nome do arquivo onde o serviço de auditoria vai salvar os dados
ARQUIVO_LOG = "audit.log"

# aqui ficam os bancos que vão participar da simulação
BANCOS = [
    "banco_a",
    "banco_b",
    "banco_c",
    "banco_d"
]