from models.cartao import Cartao
from integration.transacoes_pluggy import pegar_faturas
from rich import print
from database.conta import inserir_cartao_banco

class Conta:
    def __init__(self):
        self.cartoes = []
        self.fatura_atual, self.historico_faturas = pegar_faturas()

    def adicionar_cartao(self, card_number, user):
        if user.strip() == "" or card_number.strip() == "":
            return "Erro, dados inválidos."

        inserir_cartao_banco(card_number, user)
        
    def listar_cartoes(self):
        pass