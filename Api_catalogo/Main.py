from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector
import json

#Criado o aplicativo com a utilização do Framework Flask
app = Flask(__name__)
#Ativa o opção que identifica modificações
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#Define o caminho do Banco de Dados
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/catalogo_db"

#A extensão do SQLachemy é chamada
db = SQLAlchemy(app)

#Cria a classe Catalogo e são definidos os seus atributos
class Catalogo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(20), nullable = False)
    descricao = db.Column(db.String(100))
    preco = db.Column(db.String(12), nullable = False)
    disponibilidade = db.Column(db.Boolean, nullable = False)

    #Função que converte uma lista para o formato JSON
    def to_json_catalogo(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao, "preco": self.preco, "disponibilidade": self.disponibilidade}
    
    def to_json_catalogo_dispo(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao, "preco": self.preco}

#Função resposavel pelos responses, mostrando o status, a mensagem,e o conteudo que foram passados como parametros
def geraResponse(status, mensagem, nome_do_conteudo, conteudo, nome_segundo_conteudo=False, segundo_conteudo=False, nome_terceiro_conteudo=False, terceiro_conteudo=False):
    
    body = {}
    body[nome_do_conteudo] = conteudo
    body["mensagem"] = mensagem
    if segundo_conteudo and nome_segundo_conteudo:
        body[nome_segundo_conteudo] = segundo_conteudo
    if terceiro_conteudo and nome_terceiro_conteudo:
        body[nome_terceiro_conteudo] = terceiro_conteudo
    return Response(json.dumps(body), status=status, mimetype="application/json")
