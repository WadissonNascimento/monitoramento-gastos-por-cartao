from integration.transacoes_pluggy import pegar_transacoes
from database.transacoes import inserir_transacoes_banco

def atualizar_tabela_transacoes():
    transacoes_fechadas, _ = pegar_transacoes()
    
    inserir_transacoes_banco(transacoes_fechadas)
    
    