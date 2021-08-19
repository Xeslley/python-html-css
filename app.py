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
def depois_request():
    g.bd.close()


@app.route("/hello")
def pagina_inicial():
    return "Hello World"


