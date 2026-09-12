import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conexao_banco():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="sistema_financeiro",
            user="postgres",
            password=os.getenv("SENHA_BD"),
            port="5432"
        )
        
        cursor = conexao.cursor()
        
        return conexao, cursor
    
    except Exception as erro:
        print(f"Erro ao conectar ao banco: {erro}")
        return None, None

