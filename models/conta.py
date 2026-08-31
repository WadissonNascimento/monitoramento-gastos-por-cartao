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
        

        

    
    def exibir_cartoes(self):
        cartoes = []

        for cartao in self.cartoes:
            cartoes.append({
                "numero":cartao.numeros,
                "usuario":cartao.usuario,
                "valor_fatura_atual":cartao.valor_fatura_atual,
                "fatura_atual":cartao.fatura_atual,
                "historico_faturas":cartao.historico_faturas
            })

        return cartoes