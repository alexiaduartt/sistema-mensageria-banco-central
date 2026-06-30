@echo off
title demo sistema mensageria banco central

echo iniciando rabbitmq...
docker compose up -d

echo aguardando rabbitmq iniciar...
timeout /t 10 /nobreak > nul

echo abrindo painel do rabbitmq...
start http://localhost:15672

echo iniciando servico de auditoria...
start "servico de auditoria" cmd /k py servico_auditoria.py

echo aguardando servico de auditoria iniciar...
timeout /t 3 /nobreak > nul

echo iniciando banco_a...
start "banco_a" cmd /k py produtor_banco.py banco_a

echo iniciando banco_b...
start "banco_b" cmd /k py produtor_banco.py banco_b

echo iniciando banco_c...
start "banco_c" cmd /k py produtor_banco.py banco_c

echo tudo iniciado.
echo acesse o painel do rabbitmq com usuario guest e senha guest.
pause