from database.conexao import conexao_banco

def inserir_transacoes_banco(transacoes_fechadas):
    conexao,  cursor = conexao_banco()
    
    print(transacoes_fechadas)
    try:
        for transacao in transacoes_fechadas:
            cursor.execute('''
            INSERT INTO transacoes (
            id,
            description,
            amount,
            date,
            category,
            card_number,
            bill_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING  
            ''',
            (transacao["id"], transacao["description"], transacao["amount"], transacao["date"], transacao["category"], transacao["cardNumber"], transacao["billId"]))
            
        
        conexao.commit()
        
        return 200
    
    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao inserir transações ao banco: {str(erro)} ")
    
    
    finally:
        conexao.close()
        cursor.close()

