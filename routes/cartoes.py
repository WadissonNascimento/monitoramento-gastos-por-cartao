from flask import Blueprint, request
from services.cartao import criar_cartoes, excluir_cartao, cadastrar_cartao
import json
from excpetions import *

cartoes_bp = Blueprint("cartoes", __name__)

@cartoes_bp.post("/cartoes")
def adicionar_cartao():
    dados = request.get_json()
    
    user = dados.get("user")
    card_number = dados.get("card_number")
    
    try:
        mensagem, sucesso = cadastrar_cartao(user, card_number)

        if sucesso:
            return {"mensagem": mensagem}, 201
        
        else:
            return {"erro": mensagem}, 500

    except DadosInvalidos as erro:
        return {"erro": str(erro)}, 400
    
    except CartaoJaCadastrado as erro:
        return {"erro": str(erro)}, 409
    
    
@cartoes_bp.get("/cartoes")
def listar_cartoes(): 
    try: 
        cartoes, sucesso = criar_cartoes()
        
        dados = [cartao.to_dict() for cartao in cartoes]
            
        if sucesso:
            return dados 
        
        else:
            return {"erro":"erro inesperado"}, 500
    
    except ErroInesperado as erro:
        return {"erro":str(erro)},500

@cartoes_bp.delete("/cartoes")
def deletar_cartao():
    try:
        dados = request.get_json()

        card_number = dados.get("card_number")

        mensagem, sucesso = excluir_cartao(card_number)

        if sucesso:
            return {"", 204}

        return {"erro":mensagem}, 500

    except DadosInvalidos as erro:
        return {"erro":str(erro)}, 400

    except CartaoNaoExiste as erro:
        return {"erro":str(erro)}, 404

        

    