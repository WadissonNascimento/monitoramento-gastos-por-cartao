class Cartao:
    def __init__(self, numeros, usuario, fatura_atual, historico_faturas):
        self.numeros = numeros
        self.usuario = usuario
        self.fatura_atual = fatura_atual
        self.historico_faturas = historico_faturas

                        
    def to_dict(self):
        return {
            "numeros": self.numeros,
            "usuario": self.usuario,
            "fatura_atual": self.fatura_atual
        }
    