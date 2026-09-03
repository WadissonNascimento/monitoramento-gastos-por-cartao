from excpetions import *
from database.conta import verificar_cartao_existe, inserir_cartao_banco

def verificar_cartao(user, card_number):
    if user.strip() == "" or card_number.strip() == "":
        raise DadosInvalidos("Usuário ou cartão inválido.")
    
    if verificar_cartao_existe(card_number):
        raise CartaoJaCadastrado("O cartão ja está cadastrado.")
    
    else:
        mensagem, sucesso = inserir_cartao_banco(user, card_number)
        
        return mensagem, sucesso
        
        
    