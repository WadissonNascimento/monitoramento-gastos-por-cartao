from flask import Blueprint, request
from services.conta import verificar_cartao
from excpetions import *

cartoes_bp = Blueprint("cartoes", __name__)

@cartoes_bp.post("/cartoes")
def adicionar_cartao():
    dados = request.get_json()
    
    user = dados.get("user")
    card_number = dados.get("card_number")
    
    try:
        mensagem, sucesso = verificar_cartao(user, card_number)

        if sucesso:
            return {"mensagem": "Cartão cadastrado com sucesso."}, 201
        
        else:
            return {"erro": "Erro ao inserir cartão no banco"}, 500

    except DadosInvalidos as erro:
        return {"erro": str(erro)}, 400
    
    except CartaoJaCadastrado as erro:
        return {"erro": str(erro)}, 400