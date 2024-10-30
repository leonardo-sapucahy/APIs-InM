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
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://var.user:@#endpointRDS/clientes_db"

#A extensão do SQLachemy é chamada
db = SQLAlchemy(app)


#Cria a classe CLientes e são definidos os seus atributos
class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50), nullable = False)
    cpf =  db.Column(db.String(14), nullable = False,unique = True)
    email = db.Column(db.String(30), nullable = False,unique = True)
    senha = db.Column(db.String(20), nullable = False)
    ativo = db.Column(db.Boolean, nullable = False)
    casa = db.relationship('Enderecos', backref='dono')

    #Função que converte uma lista para o formato JSON
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "cpf": self.cpf, "email": self.email, "senha": self.senha, "ativo": self.ativo}
    #Função que converte uma lista para o formato JSON
    def to_json_ativo(self):
        return {"id": self.id, "nome": self.nome, "cpf": self.cpf, "email": self.email, "senha": self.senha}

#Cria a classe Enderecos e são definidos os seus atributos
class Enderecos(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'),nullable = False)
    rua = db.Column(db.String(30))
    numero = db.Column(db.Integer, nullable = False)
    complemento = db.Column(db.String(30))
    CEP = db.Column(db.String(8), nullable = False)
    ativo = db.Column(db.Boolean, nullable = False)

    #Função que converte uma lista para o formato JSON
    def to_json_endereco(self):
        return {"id": self.id, "id_cliente": self.id_cliente, "rua": self.rua, "numero": self.numero, "complemento": self.complemento, "CEP": self.CEP, "ativo": self.ativo}
    
    #Função que converte uma lista para o formato JSON
    def to_json_endereco_ativo(self):
        return {"id": self.id, "id_cliente": self.id_cliente, "rua": self.rua, "numero": self.numero, "complemento": self.complemento, "CEP": self.CEP}

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
