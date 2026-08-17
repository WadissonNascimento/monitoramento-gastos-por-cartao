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
            try:
                transacoes.append({
                    "id":transacao["id"],
                    "description":transacao["description"],
                    "amount":transacao["amount"],
                    "date":transacao["date"],
                    "category":transacao["category"],
                    "cardNumber":transacao["creditCardMetadata"]["cardNumber"],
                    "billId":transacao["creditCardMetadata"]["billId"],
                })
            except KeyError:
                transacoes.append({
                    "id":transacao["id"],
                    "description":transacao["description"],
                    "amount":transacao["amount"],
                    "date":transacao["date"],
                    "category":transacao["category"],
                    "cardNumber":transacao["creditCardMetadata"]["cardNumber"],
                    "status":transacao["status"],
                    "billId":transacao["creditCardMetadata"]["billForecastDate"],
                })


    return transacoes[:10]



def pegar_faturas():
    from datetime import datetime
    data_atual = datetime.now()
    mes_ano = f"{data_atual.year}-{data_atual.month:02d}"
    data_fatura_atual = data_atual.month + 1
    if data_fatura_atual == 13:
        data_fatura_atual = 1
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
    fatura_atual = {
        "fatura_mes":data_fatura_atual,
        "totalAmount":0,
        "transactions":[]
    }

    for fatura in dados["results"]:
        historico_faturas.append({
            "id":fatura["id"],
            "dueDate":fatura["dueDate"],
            "totalAmount":0,
            "transactions":[]
        })
    
    transactions = pegar_transacoes()

    for transaction in transactions:
        if mes_ano == transaction["billId"]:
            fatura_atual["transactions"].append(transaction)
            fatura_atual["totalAmount"] += transaction["amount"]
            continue

        for fatura in historico_faturas:
            if fatura["id"] == transaction["billId"]:
                fatura["transactions"].append(transaction)
                fatura["totalAmount"] += transaction["amount"]
                break
                 
        

    return fatura_atual, historico_faturas


