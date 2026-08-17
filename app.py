from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Funcionando..."


if __name__ == "__main__":
    app.run(debug=True)