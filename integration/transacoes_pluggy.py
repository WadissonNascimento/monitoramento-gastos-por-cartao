from dotenv import load_dotenv
import requests
import os
from rich import print
from excpetions import ErroInesperado

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

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)

        response.raise_for_status()
        dados =  response.json()
        return dados["apiKey"]

    except requests.exceptions.Timeout:
        raise ErroInesperado("A Pluggy demorou para responder.")

    except requests.exceptions.RequestException:
        raise ErroInesperado("Não foi possível consultar a Pluggy.")

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
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        response.raise_for_status()
        dados = response.json()

        return dados["results"][0]["id"]

    except requests.exceptions.Timeout:
        raise ErroInesperado("A Pluggy demorou para responder.")

    except requests.exceptions.RequestException:
        raise ErroInesperado("Não foi possível consultar a Pluggy.")

def pegar_transacoes():
    try:
        url_base = "https://api.pluggy.ai/v2/transactions"

        url = url_base

        headers = {
            "accept": "application/json",
            "X-API-KEY": pegar_apiKey()
        }
        params = {
            "accountId":pegar_id_cartao()
        }

        dados = []

        while True:
            response = requests.get(url, headers=headers, params=params, timeout=15)

            
            response.raise_for_status()
            resposta = response.json()

            dados.extend(resposta["results"])

            proxima_pagina = resposta["next"]

            if not proxima_pagina:
                break
            
            url = url_base + proxima_pagina
            params = None

    except requests.exceptions.Timeout:
        raise ErroInesperado("A pluggy demorou para responder.")

    except requests.exceptions.RequestException:
        raise ErroInesperado("Não foi possível consultar a Pluggy.")

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
        
    url = "https://api.pluggy.ai/bills"

    headers = {
        "accept": "application/json",
        "X-API-KEY":pegar_apiKey()
        }

    params = {
        "accountId":pegar_id_cartao()
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        response.raise_for_status()
        dados = response.json()

    except requests.exceptions.Timeout:
        raise ErroInesperado("A pluggy demorou para responder.")

    except requests.exceptions.RequestException:
        raise ErroInesperado("Não foi possível consultar a Pluggy.")

    historico_faturas = []

    for fatura in dados["results"]:
        historico_faturas.append({
            "id":fatura["id"],
            "dueDate":fatura["dueDate"],
            "totalAmount":fatura["totalAmount"]
        })
        
    return historico_faturas

