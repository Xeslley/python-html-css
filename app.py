from flask import Flask, request, session, g, redirect, \
    abort, render_template, flash
import sqlite3

# configuração
DATABASE = "blog.db"
SECRET_KEY = "pudim"

app = Flask(__name__)
# __name__ variavel do python que guarda o nome do arquivo atual

app.config.from_object(__name__)


def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()


@app.teardown_request
def depois_request(exc):
    g.bd.close()

@app.route("/")
@app.route("/entradas")
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, texto in cur.fetchall():
        entradas.append({"titulo":titulo, "texto":texto})

    return render_template("exibir_entradas.html", lista_entradas = entradas)


@app.route("/hello")
def pagina_inicial():
    return "Hello World"