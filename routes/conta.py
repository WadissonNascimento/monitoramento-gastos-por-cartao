from flask import Blueprint, request
from database.transacoes import atualizar_transacoes_banco
from database.faturas import atualizar_faturas
from integration.transacoes_pluggy import pegar_faturas, pegar_transacoes
from excpetions import ErroInesperado
import os
import hmac

conta_bp = Blueprint("conta", __name__)

@conta_bp.post("/webhook/pluggy")
def atualizar_transacões_e_faturas_banco():
    recebido = request.headers.get("Authorization", "")
    esperado = os.getenv("WEBHOOK_SECRET")

    if not esperado or not hmac.compare_digest(recebido, esperado):
        return {"erro":"Não autorizado."}, 401

    try:
        faturas = pegar_faturas()

        transacoes_fechadas, _ = pegar_transacoes()

    except ErroInesperado as erro:
        return {"erro":str(erro)}, 502

    sucesso_transacoes = atualizar_transacoes_banco(transacoes_fechadas)

    sucesso_faturas = atualizar_faturas(faturas)

    if sucesso_faturas and sucesso_transacoes:
        return {"mensagem":"Faturas e  transações atualizados com sucesso."}, 200

    return {"erro":"Erro ao salvar no banco."}, 500 