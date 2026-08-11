from rich import print
from rich.traceback import install

install()

class Conta:
    def __init__(self):
        self.cartoes = {}

    def adicionar_cartao(self, numero_cartao, nome_cartao):
        if nome_cartao.strip() == "":
            return "Erro, dados inválidos."
        

        self.cartoes[numero_cartao] = {
            "usuário":nome_cartao,
            "fatura": None,
            "transações":[]
        }
        return "Cartão adicionado com sucesso."
 
        
    def receber_transacoes(self, transacoes):
        for transacao in transacoes:
            for nome, dados in transacao.items():
                self.cartoes[dados["cartao"]]["transações"].append({
                    nome:{
                        "valor":dados["valor"],
                        "data":dados["data"],
                        "tipo":dados["tipo"]
                    }
                })

    
    def exibir_cartoes(self):
        for cartao in self.cartoes:
            self.calcular_fatura(cartao)

        return self.cartoes

    def calcular_fatura(self, numero_cartao):
        total = 0

        for transacoes in self.cartoes[numero_cartao]["transações"]:
            for nome, dados in transacoes.items():
                valor = dados["valor"]
                total += valor

        self.cartoes[numero_cartao]["fatura"] = total

        return total
                


c1 = Conta()


transacoes = [{
    "Padaria Central": {
        "cartao": 1233,
        "valor": 12.50,
        "data": "20/06/2025",
        "tipo": "Crédito"
    },

    "Posto Avenida": {
        "cartao": 1233,
        "valor": 150.00,
        "data": "20/06/2025",
        "tipo": "Crédito"
    },

    "Farmácia São Paulo": {
        "cartao": 1233,
        "valor": 37.80,
        "data": "21/06/2025",
        "tipo": "Crédito"
    },

    "McDonalds": {
        "cartao": 1233,
        "valor": 42.90,
        "data": "21/06/2025",
        "tipo": "Crédito"
    },

    "Uber01": {
        "cartao": 1233,
        "valor": 23.75,
        "data": "22/06/2025",
        "tipo": "Crédito"
    },

    "Supermercado Extra": {
        "cartao": 1233,
        "valor": 286.40,
        "data": "22/06/2025",
        "tipo": "Crédito"
    },

    "Netflix": {
        "cartao": 1233,
        "valor": 39.90,
        "data": "23/06/2025",
        "tipo": "Crédito"
    },

    "Shopee": {
        "cartao": 1233,
        "valor": 89.99,
        "data": "23/06/2025",
        "tipo": "Crédito"
    },

    "Restaurante do Zé": {
        "cartao": 1233,
        "valor": 64.50,
        "data": "24/06/2025",
        "tipo": "Crédito"
    },

    "iFood": {
        "cartao": 1267,
        "valor": 54.90,
        "data": "25/06/2025",
        "tipo": "Crédito"
    },

    "Amazon": {
        "cartao": 1267,
        "valor": 129.99,
        "data": "25/06/2025",
        "tipo": "Crédito"
    },

    "Drogaria Popular": {
        "cartao": 1267,
        "valor": 31.40,
        "data": "26/06/2025",
        "tipo": "Crédito"
    },

    "Posto Shell": {
        "cartao": 1267,
        "valor": 180.00,
        "data": "26/06/2025",
        "tipo": "Crédito"
    },

    "Burger King": {
        "cartao": 1267,
        "valor": 38.50,
        "data": "27/06/2025",
        "tipo": "Crédito"
    },

    "Uber02": {
        "cartao": 1267,
        "valor": 27.80,
        "data": "27/06/2025",
        "tipo": "Crédito"
    },

    "Assaí Atacadista": {
        "cartao": 1267,
        "valor": 243.65,
        "data": "28/06/2025",
        "tipo": "Crédito"
    },

    "Spotify": {
        "cartao": 1267,
        "valor": 21.90,
        "data": "28/06/2025",
        "tipo": "Crédito"
    },

    "Mercado Livre": {
        "cartao": 1267,
        "valor": 74.99,
        "data": "29/06/2025",
        "tipo": "Crédito"
    },

    "Pizzaria Napoli": {
        "cartao": 1267,
        "valor": 68.00,
        "data": "29/06/2025",
        "tipo": "Crédito"
    }
}]

print(c1.adicionar_cartao(1233, "Wadisson"))
print(c1.adicionar_cartao(1267, "Emilly"))
c1.receber_transacoes(transacoes)
print(c1.exibir_cartoes())