from services.cartao import Cartao
from integration.transacoes_pluggy import pegar_faturas
from rich import print

class Conta:
    def __init__(self):
        self.cartoes = []
        self.fatura_atual, self.historico_faturas = pegar_faturas()

    def adicionar_cartao(self, numero_cartao, usuario):
        if usuario.strip() == "" or numero_cartao.strip() == "":
            return "Erro, dados inválidos."

        cartao = Cartao(numero_cartao, usuario, self.fatura_atual, self.historico_faturas)
        self.cartoes.append(cartao)

    
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


c1 = Conta() 
c1.adicionar_cartao("1985", "Emilly")
c1.adicionar_cartao("6603", "Wadisson")
c1.adicionar_cartao("8032", "Wadisson")
c1.adicionar_cartao("4078", "Wadisson") 
c1.adicionar_cartao("0478", "Wadisson")   
print(c1.exibir_cartoes())
