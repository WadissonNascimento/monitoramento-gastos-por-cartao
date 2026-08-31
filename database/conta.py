from database.conexao import conexao_banco

def inserir_cartao_banco(card_number, user):
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
    
    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao inserir cartão ao banco: {str(erro)}")
    
    finally:
        conexao.close()
        cursor.close()