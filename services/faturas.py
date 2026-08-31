from integration.transacoes_pluggy import pegar_faturas, pegar_transacoes
from database.faturas import inserir_faturas
from datetime import datetime

def atualizar_historico_faturas():
    historico_faturas = pegar_faturas()
    
    inserir_faturas(historico_faturas)
    
def calcular_fatura_atual():
    _ , transacoes_em_aberto = pegar_transacoes()
    
    data_atual = datetime.now()
    mes_ano = f"{data_atual.year}-{data_atual.month:02d}"
    data_fatura_atual = data_atual.month + 1
    
    
    fatura_atual = {
        "bill": data_fatura_atual,
        "totalAmount": 0,
        "transactions": []
    }
    
    if data_fatura_atual == 13:
        data_fatura_atual = 1
    
    
    for transacao in transacoes_em_aberto:
        if transacao["billId"] == mes_ano:
            fatura_atual["totalAmount"] += transacao["amount"]
            fatura_atual["transactions"].append(transacao)

    return fatura_atual

