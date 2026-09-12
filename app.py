from flask import Flask
import os
from database.tabelas import iniciar_banco
from routes.cartoes import cartoes_bp
from routes.conta import conta_bp

iniciar_banco()

app = Flask(__name__)

app.register_blueprint(cartoes_bp)
app.register_blueprint(conta_bp)

@app.route("/")
def home():
    return "Funcionando..."



if __name__ == "__main__":
    app.run(debug=True)