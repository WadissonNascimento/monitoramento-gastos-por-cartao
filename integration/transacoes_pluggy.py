from dotenv import load_dotenv
import requests
import os
from rich import print

load_dotenv()

def pegar_apiKey():
    url = "https://api.pluggy.ai/auth"

    payload = {
        "clientId": os.getenv("CLIENTE_ID"),
        "clientSecret": os.getenv("CLIENTE_SECRET")
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    dados =  response.json()
    return dados["apiKey"]

def pegar_id_cartao():
    api_key = pegar_apiKey()

    url = "https://api.pluggy.ai/accounts"

    headers = {
        "accept":"application/json",
        "X-API-KEY":api_key
    }

    params = {
        "itemId":os.getenv("ITEM_ID"),
        "type":"CREDIT"
    }

    response = requests.get(url, headers=headers, params=params)

    dados = response.json()

    return dados["results"][0]["id"]


def pegar_transacoes():
    url = "https://api.pluggy.ai/v2/transactions"

    headers = {
        "accept": "application/json",
        "X-API-KEY": pegar_apiKey()
    }
    params = {
        "accountId":pegar_id_cartao()
    }

    response = requests.get(url, headers=headers, params=params)


    dados = response.json()

    dados = dados["results"]

    transacoes_fechadas = []
    
    transacoes_em_aberto = []

    for transacao in dados:
        if transacao["type"] == "DEBIT":
            try:
                transacoes_fechadas.append({
                    "id":transacao["id"],
                    "description":transacao["description"],
                    "amount":transacao["amount"],
                    "date":transacao["date"],
                    "category":transacao["category"],
                    "cardNumber":transacao["creditCardMetadata"]["cardNumber"],
                    "billId":transacao["creditCardMetadata"]["billId"],
                })
            except KeyError:
                transacoes_em_aberto.append({
                    "id":transacao["id"],
                    "description":transacao["description"],
                    "amount":transacao["amount"],
                    "date":transacao["date"],
                    "category":transacao["category"],
                    "cardNumber":transacao["creditCardMetadata"]["cardNumber"],
                    "status":transacao["status"],
                    "billId":transacao["creditCardMetadata"]["billForecastDate"],
                })


    return transacoes_fechadas, transacoes_em_aberto



def pegar_faturas():
    from datetime import datetime
        
    url = "https://api.pluggy.ai/bills"

    headers = {
        "accept": "application/json",
        "X-API-KEY":pegar_apiKey()
        }

    params = {
        "accountId":pegar_id_cartao()
    }

    response = requests.get(url, headers=headers, params=params)

    dados = response.json()

    historico_faturas = []

    for fatura in dados["results"]:
        historico_faturas.append({
            "id":fatura["id"],
            "dueDate":fatura["dueDate"],
            "totalAmount":fatura["totalAmount"]
        })
        
    return historico_faturas
