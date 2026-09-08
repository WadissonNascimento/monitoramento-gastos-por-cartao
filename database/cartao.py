from database.conexao import conexao_banco
from rich import print

def buscar_cartoes():
    conexao, cursor = conexao_banco()
    
    try:
        cursor.execute('''
        SELECT usuario, card_number
        FROM cartoes     
        ''')

        cartoes = cursor.fetchall()
        
        return cartoes, True
    
    except Exception as erro:
        return f"erro: {str(erro)}", False
    
    finally:
        conexao.close()
        cursor.close()


def buscar_billID_faturas():
    conexao, cursor = conexao_banco()
    
    try:
        cursor.execute('''
        SELECT bill_id, due_date
        FROM faturas
        ''')
        
        resultado = cursor.fetchall()
        
        return resultado, True
    
    except Exception as erro:
        return f"erro: {str(erro)}", False

    finally:
        cursor.close()
        conexao.close()
    
def buscar_historico_faturas(card_number):
    conexao, cursor = conexao_banco()
    
    try:
        bill_ID_datas, sucesso = buscar_billID_faturas()
        
        historico_faturas = []
        
        for conjunto in bill_ID_datas:
            billID, data = conjunto
            
            cursor.execute('''
            SELECT *
            FROM transacoes
            WHERE bill_id = %s
                AND card_number = %s            
            ''',(billID, card_number))
        
            
            resultado = cursor.fetchall()
            
            total = 0
            
            transacoes = []
            
            for transacao in resultado:
                id_transacao, description, amount, date, category, card_number_bd, bill_id = transacao
                
                total += amount
                
                transacoes.append({
                    "id": id_transacao,
                    "description": description,
                    "amount": f"R$ {amount:.2f}".replace(".", ","),
                    "date": date.strftime("%d/%m/%Y"),
                    "category": category,
                    "card_number": card_number_bd,
                    "bill_id": bill_id
                })
                        
            historico_faturas.append({
                "fatura":data.strftime("%d/%m/%Y"),
                "total": f"R$ {total:.2f}".replace(".", ","),
                "transacoes": transacoes
            })
        
        return historico_faturas, True
        
    
    except Exception as erro:
        return f"Erro:{str(erro)}", False
    
    finally: 
        conexao.close()
        cursor.close()
