from database.conexao import conexao_banco

def inserir_faturas(faturas):
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
        
        return 200
    
    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao inserir informações na tabela: {erro}")
    
    finally:
        conexao.close()
        cursor.close()