from flask import Blueprint, request
from services.conta import verificar_cartao
from services.cartao import criar_cartoes
import json
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
        return {"erro": str(erro)}, 409
    
    
@cartoes_bp.get("/cartoes")
def listar_cartoes(): 
    try: 
        cartoes, sucesso = criar_cartoes()
        
        dados = [cartao.to_dict() for cartao in cartoes]
        
        with open("cartoes.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            
        if sucesso:
            return dados 
        
        else:
            return {"erro":"erro inesperado"}, 500
    
    except ErroInesperado as erro:
        return {"erro":str(erro)},500
    