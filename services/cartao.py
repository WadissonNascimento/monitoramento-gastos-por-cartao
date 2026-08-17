class Cartao:
    def __init__(self, numeros, usuario, fatura_atual, historico_faturas):
        self.numeros = numeros
        self.usuario = usuario
        self.valor_fatura_atual = 0
        self.fatura_atual = []
        self.historico_faturas = []

        self.separar_faturas(fatura_atual, historico_faturas)

    def separar_faturas(self, fatura_atual, historico_faturas):

        for transacao in fatura_atual["transactions"]:
            if transacao["cardNumber"] == self.numeros:
                self.fatura_atual.append(transacao)
                self.valor_fatura_atual += transacao["amount"]

        for fatura in historico_faturas:
            for transacao in fatura["transactions"]:
                if transacao["cardNumber"] == self.numeros:
                    self.historico_faturas.append(fatura)
                        

    