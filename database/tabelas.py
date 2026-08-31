from database.conexao import conexao_banco

def iniciar_banco():
    conexao, cursor = conexao_banco()
    
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS faturas (
        id_fatura SERIAL PRIMARY KEY,
        bill_id VARCHAR(100) UNIQUE,
        due_date DATE NOT NULL,
        total_amount NUMERIC(10, 2) NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
        id VARCHAR(100) PRIMARY KEY, 
        description VARCHAR(50) NOT NULL,
        amount NUMERIC(10, 2) NOT NULL,
        date DATE NOT NULL,
        category VARCHAR(50) NOT NULL,
        card_number VARCHAR(4) NOT NULL,
        bill_id VARCHAR(100) NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartoes (
        id SERIAL PRIMARY KEY,
        usuario VARCHAR(20) NOT NULL,
        card_number VARCHAR(4) UNIQUE
        )          
        ''')
        
        conexao.commit()
        
    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao iniciar banco de dados: {erro}")
    
    finally:
        conexao.close()
        cursor.close()

