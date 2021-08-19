from flask import Flask

app = Flask(__name__)
# __name__ variavel do python que guarda o nome do arquivo atual

@app.route("/hello")
def pagina_inicial():
    return "Hello World"

@app.route("/amor")
def pagina_amor():
    return "<h1>Te Amo!!!</h1>"

