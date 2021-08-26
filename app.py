from flask import Flask, request, session, g, redirect, \
    abort, render_template, flash, url_for
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

@app.route("/inserir", methods = ["POST"])
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO  ENTRADAS(TITULO, TEXTO) values ( ?, ?)"
    g.bd.execute(sql, request.form('campoTitulo'), request.form('campoTexto'))
    g.bd.commit()
    return redirect(url_for("exibir_entradas"))

@app.route("/logout")
def logout():
    session.pop('logado', None)
    return redirect(url_for("exibir_entradas"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    erro = None
    print("foi POST")
    if request.method == "POST":
        if request.form["campoUsuario"] != 'admin' or request.form["campoSenha"] != 'admin':
            erro = "Senha ou Usuário inválidos"
        else:
            session['logado'] = True
            return redirect(url_for("exibir_entradas"))

    return render_template('login.html', erro = erro)