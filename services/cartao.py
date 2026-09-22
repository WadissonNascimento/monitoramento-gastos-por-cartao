from models.cartao import Cartao
from database.cartao import buscar_cartoes, buscar_historico_faturas
from database.conta import verificar_cartao_existe, excluir_cartao_banco
from integration.transacoes_pluggy import pegar_transacoes
from datetime import datetime
from dateutil.relativedelta import relativedelta
from excpetions import *
from excpetions import *
from database.conta import verificar_cartao_existe, inserir_cartao_banco


def criar_cartoes():
    cartoes, sucesso_cartoes = buscar_cartoes()

    objetos = []
    
    data_atual = datetime.now()
    mes_ano = data_atual.strftime("%Y-%m")
    mes_ano_anterior = (data_atual - relativedelta(months=1)).strftime("%Y-%m")
     
    mes_atual = data_atual.month
    data_da_fatura = mes_atual + 1
    
    if data_da_fatura == 13:
        data_da_fatura = 1
    
    if sucesso_cartoes:
        _ , transacoes_em_aberto = pegar_transacoes()
        
        for cartao in cartoes:
            usuario, card_number = cartao
            
            fatura_atual = {
                "mes-fatura":data_da_fatura,
                "valor":0,
                "transacoes":[]
            }       
            
            for transacao in transacoes_em_aberto:
                if transacao["billId"] == mes_ano and transacao["cardNumber"] == card_number:
                    fatura_atual["valor"] += transacao["amount"]
                    fatura_atual["transacoes"].append(transacao)
                
                elif transacao["billId"] == mes_ano_anterior and transacao["cardNumber"] == card_number:
                    fatura_atual["valor"] += transacao["amount"]
                    fatura_atual["transacoes"].append(transacao)
                    
            historico_faturas, sucesso = buscar_historico_faturas(card_number)
            
            if sucesso:
                objeto = Cartao(card_number, usuario,fatura_atual,historico_faturas)
                objetos.append(objeto)
                
            else: 
                raise ErroInesperado("Erro inesperado ao consultar o banco de dados.")
            
        
        return objetos, True
    
    else:
        return objetos, False
            

def excluir_cartao(card_number):
    if not card_number:
        raise DadosInvalidos("Cartão inválido.")

    if card_number.strip() == "":
        raise DadosInvalidos("Cartão inválido.")

    cartao_existe = verificar_cartao_existe(card_number)

    if cartao_existe:
        mensagem, sucesso = excluir_cartao_banco(card_number)

        return mensagem, sucesso

    raise CartaoNaoExiste("Cartão não cadastrado.")


def cadastrar_cartao(user, card_number):
    if not user or not card_number:
        raise DadosInvalidos("Usuário ou cartão inválido.")
    
    if user.strip() == "" or card_number.strip() == "":
        raise DadosInvalidos("Usuário ou cartão inválido.")
    
    if verificar_cartao_existe(card_number):
        raise CartaoJaCadastrado("O cartão ja está cadastrado.")
    
    else:
        mensagem, sucesso = inserir_cartao_banco(user, card_number)
        
        return mensagem, sucesso
        
        