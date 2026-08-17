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

    transacoes = []

    for transacao in dados:
        if transacao["type"] == "DEBIT":
            transacoes.append({
                "id":transacao["id"],
                "description":transacao["description"],
                "amount":transacao["amount"],
                "date":transacao["date"],
                "category":transacao["category"],
                "cardNumber":transacao["creditCardMetadata"]["cardNumber"]
            })

    return transacoes
