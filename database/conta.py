from database.conexao import conexao_banco

def inserir_cartao_banco(user, card_number):
    conexao, cursor = conexao_banco()
    
    try:
        cursor.execute('''
        INSERT INTO cartoes (
        usuario,
        card_number
        )
        VALUES(%s, %s)
        ''',
        (user, card_number))


        conexao.commit()
        return f"Cartão adicionado com sucesso.", True
    
    except Exception as erro:
        conexao.rollback()
        return f"Erro ao inserir cartão ao banco: {str(erro)}", False
    
    finally:
        conexao.close()
        cursor.close()
    
    
def verificar_cartao_existe(card_number):
    conexao, cursor = conexao_banco()
    
    try:
        cursor.execute('''
        SELECT *
        FROM cartoes
        WHERE card_number = %s
        ''',
        (card_number,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            return True
        
        else:
            return False
        
    except Exception as erro:
        conexao.rollback()
        print(f"erro:{str(erro)}")
    
    finally:
        conexao.close()
        cursor.close()