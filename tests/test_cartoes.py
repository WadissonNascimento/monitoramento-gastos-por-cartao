from unittest.mock import Mock

import pytest
import os
from app import app
from database.conexao import conexao_banco
from database.conta import inserir_cartao_banco, verificar_cartao_existe
from excpetions import ErroInesperado
from integration.transacoes_pluggy import pegar_transacoes, pegar_faturas


# Fixtures — preparação e limpeza dos testes


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as  client:
        yield client


@pytest.fixture
def banco_limpo():
    conexao, cursor = conexao_banco()

    try:
        cursor.execute("DELETE FROM cartoes")
        conexao.commit()

        yield

    finally:
        cursor.execute("DELETE FROM cartoes")
        conexao.commit()
        cursor.close()
        conexao.close()


# Cadastro — POST /cartoes


def test_cadastro_cartao(client, banco_limpo):
    dados = {
        "user":"wadisson",
        "card_number": "2200"
    }

    response1 = client.post(
        "/cartoes", json=dados
    )

    response2 = client.post(
        "/cartoes",
        json=dados
    )

    assert response1.status_code == 201
    assert response2.status_code == 409


@pytest.mark.parametrize("dados", [
    {},
    {"card_number": "3092"},
    {"user": "wadisson"},
    {"user": None, "card_number": "3092"},
    {"user": "", "card_number": "3092"},
    {"user": "   ", "card_number": "3092"},
    {"user": "wadisson", "card_number": None},
    {"user": "wadisson", "card_number": ""},
    {"user": "wadisson", "card_number": "   "},
])

def test_cadastro_com_dados_obrigatorio_faltando(client, dados):
    response = client.post(
        "/cartoes",
        json=dados
        )

    assert response.status_code == 400


def test_falha_ao_cadastrar_cartao(client, monkeypatch):
    erro = Mock(
        return_value=("erro ao inserir cartão no banco", False)
    )

    monkeypatch.setattr(
        "routes.cartoes.cadastrar_cartao",
        erro
    )

    response = client.post(
        "/cartoes",
        json = {
            "card_number":"6603"
        }
    )

    assert response.status_code == 500
    assert response.get_json() == {"erro":"erro ao inserir cartão no banco"}


# Listagem — GET /cartoes


def test_listar_cartoes_com_cartoes_cadastrados(client, banco_limpo):
    inserir_cartao_banco("wadisson", "6603")

    response = client.get(
        "/cartoes"
    )

    dados = response.get_json()

    assert response.status_code == 200
    assert len(dados) == 1


def test_listar_cartoes_com_banco_vazio(client, banco_limpo):

    response = client.get(
        "/cartoes"
    )

    dados = response.get_json()

    assert response.status_code == 200
    assert len(dados) == 0


def test_listar_cartoes_retornando_false(client, monkeypatch):
    erro = Mock(
        return_value=("erro inesperado", False)
    )

    monkeypatch.setattr(
        "routes.cartoes.criar_cartoes",
        erro
    )

    response = client.get(
        "/cartoes"
    )

    assert response.status_code == 500
    assert response.get_json() == {"erro":"erro inesperado"}


# Exclusão — DELETE /cartoes


def test_deletar_cartao_existente(client, banco_limpo):
    dados_cartao = {
            "card_number":"6603"
        }

    inserir_cartao_banco("wadisson","6603")

    response = client.delete(
        "/cartoes",
        json=dados_cartao
    )


    assert response.status_code == 204
    assert verificar_cartao_existe("6603") is False


def test_deletar_cartao_inexistente(client, banco_limpo):

    dados_cartao = {
        "card_number":"6603"
    }

    response = client.delete(
        "/cartoes",
        json=dados_cartao
    )

    assert response.status_code == 404


@pytest.mark.parametrize("dados",[
    {"card_number":""},
    {"card_number": None},
    {"card_number":"  "}
])

def test_excluir_cartoes_json_incorreto(client, dados):
    response = client.delete(
        "/cartoes",
        json=dados
    )

    assert response.status_code == 400


def test_excluir_cartao_erro(client, monkeypatch):
    excluir = Mock(
        return_value=("Erro ao excluir cartão.", False)
    )

    monkeypatch.setattr(
        "routes.cartoes.excluir_cartao",
        excluir
    )

    response = client.delete(
        "/cartoes",
        json={
            "card_number":"6603"
        }
    )

    assert response.status_code == 500
    assert response.get_json() == {
        "erro": "Erro ao excluir cartão."
    }


def test_webhook_falha_ao_buscar_transacoes(client, monkeypatch):
    monkeypatch.setattr(
        "routes.conta.pegar_faturas",
        Mock(return_value=[])
    )

    monkeypatch.setattr(
        "routes.conta.pegar_transacoes",
        Mock(side_effect=ErroInesperado(
            "Não foi possível consultar a Pluggy."
        ))
    )

    salvar_transacoes = Mock()
    salvar_faturas = Mock()

    monkeypatch.setattr(
        "routes.conta.atualizar_faturas",
        salvar_faturas
    )

    monkeypatch.setattr(
        "routes.conta.atualizar_transacoes_banco",
        salvar_transacoes
    )

    response = client.post(
        "/webhook/pluggy",
         headers={
            "Authorization": os.getenv("WEBHOOK_SECRET")
        }
        )

    assert response.status_code == 502
    assert response.get_json() == {
        "erro":"Não foi possível consultar a Pluggy."
    }

    salvar_transacoes.assert_not_called()
    salvar_faturas.assert_not_called()


def test_transacoes_pluggy_devolve_mais_de_uma_pagina(monkeypatch):
    # 1. Prepara duas páginas: uma transação fechada e outra aberta.
    pagina_1 = {
        "results": [
            {
                "id": "transacao_1",
                "description": "Mercado",
                "amount": 100.50,
                "date": "2026-09-19",
                "category": "Supermercado",
                "type": "DEBIT",
                "status": "POSTED",
                "creditCardMetadata": {
                    "cardNumber": "1234",
                    "billId": "2026-09"
                }
            }
        ],
        "next": "qualquer_coisa"
    }


    pagina_2 = {
        "results": [
            {
                "id": "transacao_2",
                "description": "Uber",
                "amount": 35.90,
                "date": "2026-09-20",
                "category": "Transporte",
                "type": "DEBIT",
                "status": "PENDING",
                "creditCardMetadata": {
                    "cardNumber": "1234",
                    "billForecastDate": "2026-10"
                }
            }
        ],
        "next": None
    }



    # 2. Evita chamadas reais para autenticação e busca da conta.
    monkeypatch.setattr(
        "integration.transacoes_pluggy.pegar_apiKey",
        Mock(return_value="chave-teste")
    )
    monkeypatch.setattr(
        "integration.transacoes_pluggy.pegar_id_cartao",
        Mock(return_value="conta-teste")
    )

    # 3. Simula as respostas HTTP: .json() devolve a página preparada.
    resposta_1 = Mock()
    resposta_1.json.return_value = pagina_1

    resposta_2 = Mock()
    resposta_2.json.return_value = pagina_2

    # A primeira chamada recebe resposta_1; a segunda recebe resposta_2.
    buscar = Mock(side_effect=[resposta_1, resposta_2])
    monkeypatch.setattr(
        "integration.transacoes_pluggy.requests.get",
        buscar
    )

    # 4. Executa a função real, incluindo o while da paginação.
    fechadas, abertas = pegar_transacoes()

    # 5. Confere que as duas páginas foram processadas e separadas.
    assert len(fechadas) == 1
    assert fechadas[0]["id"] == "transacao_1"
    assert len(abertas) == 1
    assert abertas[0]["id"] == "transacao_2"

    # 6. Confere que parou após duas chamadas e seguiu o cursor recebido.
    assert buscar.call_count == 2
    segunda_chamada = buscar.call_args_list[1]
    assert segunda_chamada.args[0] == (
        "https://api.pluggy.ai/v2/transactions" + pagina_1["next"]
    )
    assert segunda_chamada.kwargs["params"] is None


def test_request_webhook_Authorization(client):
    response  = client.post("/webhook/pluggy")

    response1 = client.post("/webhook/pluggy", headers={
        "Authorization":os.getenv("WEBHOOK_SECRET")
    })

    assert response.status_code  == 401
    assert response1.status_code == 200



def test_historico_faturas_paginacao(monkeypatch):
    pagina1 = {
    'total': 13,
    'totalPages': 2,
    'page': 1,
    'results': [
        {
            'id': 'ed241651-9bb5-40e8-9b30-a5000b65331c',
            'dueDate': '2026-09-07T00:00:00.000Z',
            'billClosingDate': '2026-08-31T00:00:00.000Z',
            'totalAmount': 3285.35,
            'totalAmountCurrencyCode': 'BRL',
            'minimumPaymentAmount': 353.92,
            'allowsInstallments': False,
            'financeCharges': [{'id': '1981b036-a0e2-4f5f-86b2-98e9fb55cda3', 'type': 'OTHER', 'amount': 0, 'currencyCode': 'BRL', 'additionalInfo': 'OUTROS'}],
            'payments': [
                {
                    'id': '45192c91-9dca-4d8b-997d-1669e2e6de6a',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-08-05T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 390.05,
                    'currencyCode': 'BRL'
                }
            ],
            'createdAt': '2026-09-01T16:14:31.620Z',
            'updatedAt': '2026-09-21T22:13:32.130Z'
        },
        {
            'id': 'd643fa46-96c7-4b75-bca8-8b4a49b769f5',
            'dueDate': '2026-08-07T00:00:00.000Z',
            'billClosingDate': '2026-07-31T00:00:00.000Z',
            'totalAmount': 390.05,
            'totalAmountCurrencyCode': 'BRL',
            'minimumPaymentAmount': 39,
            'allowsInstallments': False,
            'financeCharges': [{'id': '2e11b51d-dff8-4c3d-8138-1b969391beeb', 'type': 'OTHER', 'amount': 0, 'currencyCode': 'BRL', 'additionalInfo': 'OUTROS'}],
            'payments': [
                {
                    'id': '28443f9f-c7f7-4c33-a13a-833b2aa2d4ff',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-06-30T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 230,
                    'currencyCode': 'BRL'
                },
                {
                    'id': 'a3cab945-fd75-48b0-84aa-060e042d49b4',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-07-03T00:00:00.000Z',
                    'paymentMode': 'BANK_SLIP',
                    'amount': 1037,
                    'currencyCode': 'BRL'
                }
            ],
            'createdAt': '2026-08-14T09:36:39.979Z',
            'updatedAt': '2026-09-21T22:13:32.137Z'
        }
    ]}

    pagina2 = {
    'total': 13,
    'totalPages': 2,
    'page': 2,
    'results': [
        {
            'id': '6cd78aa4-d6d6-4b36-8680-756d9ebb2320',
            'dueDate': '2026-07-07T00:00:00.000Z',
            'billClosingDate': '2026-06-30T00:00:00.000Z',
            'totalAmount': 1036.6,
            'totalAmountCurrencyCode': 'BRL',
            'minimumPaymentAmount': 103.66,
            'allowsInstallments': False,
            'financeCharges': [{'id': '2ca959ea-be69-424b-b36c-85198cbb4c2a', 'type': 'OTHER', 'amount': 0, 'currencyCode': 'BRL', 'additionalInfo': 'OUTROS'}],
            'payments': [
                {
                    'id': 'e30e42c4-2d33-4c26-a62f-3d69afd2cecf',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-06-03T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 1418.36,
                    'currencyCode': 'BRL'
                }
            ],
            'createdAt': '2026-08-14T09:36:40.090Z',
            'updatedAt': '2026-09-07T03:06:29.835Z'
        },
        {
            'id': '40ddba93-dd72-4d7e-a144-4f90783f6372',
            'dueDate': '2026-06-07T00:00:00.000Z',
            'billClosingDate': '2026-05-29T00:00:00.000Z',
            'totalAmount': 1418.36,
            'totalAmountCurrencyCode': 'BRL',
            'minimumPaymentAmount': 141.83,
            'allowsInstallments': False,
            'financeCharges': [{'id': '46fafb40-a2bf-4850-831b-07fdbd1acd24', 'type': 'OTHER', 'amount': 0, 'currencyCode': 'BRL', 'additionalInfo': 'OUTROS'}],
            'payments': [
                {
                    'id': 'f3e181ca-7f01-4860-9213-eec5307b5c54',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-04-30T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 315.02,
                    'currencyCode': 'BRL'
                },
                {
                    'id': '593ce95a-8246-4b50-beb2-1723ff7c6c4f',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-05-05T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 427.38,
                    'currencyCode': 'BRL'
                },
                {
                    'id': '81cde574-0bfe-4604-8029-fad1797d0024',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-05-11T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 282.04,
                    'currencyCode': 'BRL'
                },
                {
                    'id': 'bafb4c4d-4de0-4277-903a-b75d1ce9d9d1',
                    'valueType': 'FULL_PAYMENT',
                    'paymentDate': '2026-05-27T00:00:00.000Z',
                    'paymentMode': 'DEBIT_ACCOUNT',
                    'amount': 382.82,
                    'currencyCode': 'BRL'
                }
            ],
            'createdAt': '2026-08-14T09:36:40.153Z',
            'updatedAt': '2026-08-14T09:36:40.153Z'
        }
    ]}

    monkeypatch.setattr(
        "integration.transacoes_pluggy.pegar_apiKey",
        Mock(return_value="chave_teste")
    )

    monkeypatch.setattr(
        "integration.transacoes_pluggy.pegar_id_cartao",
        Mock(return_value="id-teste")
    )

    resposta1 = Mock()
    resposta1.json.return_value = pagina1

    resposta2 = Mock()
    resposta2.json.return_value = pagina2

    buscar = Mock(side_effect=[resposta1, resposta2])

    monkeypatch.setattr(
        "integration.transacoes_pluggy.requests.get",
        buscar
    )

    historico_de_faturas = pegar_faturas()

    assert buscar.call_count == 2
    assert len(historico_de_faturas) == 4


def test_historico_de_faturas(client):
    response = client.get(
        "/historico_faturas"
    )

    assert response.status_code == 200
    assert response.is_json
