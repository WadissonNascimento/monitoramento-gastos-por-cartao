from services.cartao import Cartao
from integration.transacoes_pluggy import pegar_transacoes
from rich import print

class Conta:
    def __init__(self):
        self.cartoes = []

    def adicionar_cartao(self, numero_cartao, usuario):
        if usuario.strip() == "" or numero_cartao.strip() == "":
            return "Erro, dados inválidos."

        cartao = Cartao(numero_cartao, usuario)
        self.cartoes.append(cartao)
 
        
    def separar_transacoes(self, transacoes):
        for transacao in transacoes:
            numero_cartao = transacao["cardNumber"]
            for cartao in self.cartoes:
                if numero_cartao == cartao.numeros:
                    cartao.transacoes.append(transacao)
            


    
    def exibir_cartoes(self):
        cartoes = []

        for cartao in self.cartoes:
            cartoes.append({
                "numero":cartao.numeros,
                "usuario":cartao.usuario,
                "fatura":cartao.fatura,
                "transacoes":cartao.transacoes
            })

        return cartoes


transacoes = pegar_transacoes()
c1 = Conta() 
c1.adicionar_cartao("4078", "Emilly")
c1.adicionar_cartao("0478", "Wadisson")  
c1.separar_transacoes(transacoes)
print(c1.exibir_cartoes())
