class Cartao:
    def __init__(self, numeros, usuario):
        self.numeros = numeros
        self.usuario = usuario
        self.fatura = 0
        self.transacoes = []
