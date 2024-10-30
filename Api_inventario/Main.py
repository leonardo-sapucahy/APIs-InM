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

#Cria a classe Inventario e são definidos os seus atributos
class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_produto = db.Column(db.Integer, nullable= False)
    id_cliente = db.Column(db.Integer, nullable = False)
    
    #Função que converte uma lista para formato JSON
    def to_json_inventario(self):
        return {"id": self.id, "id_cliente": self.id_cliente, "id_produto": self.id_produto}

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
