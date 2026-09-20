from database.conexao import conexao_banco
from integration.transacoes_pluggy import pegar_faturas

def atualizar_faturas(faturas):
    conexao, cursor = conexao_banco()
    
    try:
        for fatura in faturas:
            cursor.execute('''
            INSERT INTO faturas(
            bill_id,
            due_date,
            total_amount
            )       
            VALUES (%s, %s, %s)
            ON CONFLICT (bill_id) DO NOTHING    
            ''',
            (fatura["id"], fatura["dueDate"], fatura["totalAmount"]))
        
        conexao.commit()
        
        return True
    
    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao inserir informações na tabela: {erro}")
        return False
    
    finally:
        conexao.close()
        cursor.close()
