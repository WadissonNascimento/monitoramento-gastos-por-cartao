from flask import Flask
import os
from database.tabelas import iniciar_banco

iniciar_banco()

app = Flask(__name__)



@app.route("/")
def home():
    return "Funcionando..."


if __name__ == "__main__":
    app.run(debug=True)