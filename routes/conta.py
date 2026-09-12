from flask import Blueprint

conta_bp = Blueprint("conta", __name__)

@conta_bp.post("/webhook/pluggy")
def atualizar_transacões_e_faturas_banco():
    pass