from database.conexao import conexao_banco

def atualizar_transacoes_banco(transacoes_fechadas):
    conexao,  cursor = conexao_banco()
    
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

        return True
           
    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao inserir transações ao banco: {str(erro)} ", False)
        return False
    
    
    finally:
        conexao.close()
        cursor.close()

