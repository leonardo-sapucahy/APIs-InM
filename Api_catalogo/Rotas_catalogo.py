from Main import *
from Gateway import *
import requests

URL_inventario = 'http://127.0.0.1:5002/inventario/'

#Define a rota da home
@app.route("/", methods=["GET"])
@auth.login_required
def Inicial():
    return "Olá, {}!".format(auth.current_user())

# Seleciona todos os produtos
@app.route("/catalogo", methods=["GET"])
@auth.login_required
def seleciona_catalogo():
    try:
        catalogo_objeto = db.session.query(Catalogo).filter(Catalogo.disponibilidade == 1).all()
        catalogo_json = [catalogo.to_json_catalogo_dispo() for catalogo in catalogo_objeto]
        return geraResponse(200, "ok", "catalogo", catalogo_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "catalogo", {})
    
#Seleciona Individualmente um produto do catalogo pelo ID
@app.route("/catalogo/<id>", methods=["GET"])
@auth.login_required
def seleciona_produto(id):
    try:
        produto_objeto = db.session.query(Catalogo).filter(Catalogo.id == id, Catalogo.disponibilidade == 1).first()
        produto_json = produto_objeto.to_json_catalogo_dispo()

        return geraResponse(200, "ok", "produto", produto_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "produto", {})

#Cadastrar um novo produto
@app.route("/catalogo", methods=["POST"])
@auth.login_required    
def cadastra_produto():

    body = request.get_json()  
    try:
        produto = Catalogo(nome = body["nome"], descricao = body["descricao"], preco = body["preco"], disponibilidade = body["disponibilidade"])
        produto_ja_cadastrado = db.session.query(Catalogo).filter(Catalogo.nome == body["nome"]).first()
        if produto_ja_cadastrado != None and produto_ja_cadastrado.disponibilidade == 0:
            produto_ja_cadastrado.descricao = body["descricao"]
            produto_ja_cadastrado.preco = body["preco"]
            produto_ja_cadastrado.disponibilidade = body["disponibilidade"]
            produto = produto_ja_cadastrado
        elif produto_ja_cadastrado != None and produto_ja_cadastrado.disponibilidade == 1:
            return geraResponse(400, "Produto já existe", produto_ja_cadastrado.id, {})
        db.session.add(produto)
        db.session.commit()
        return geraResponse(201, "Produto cadastrado com sucesso", "produto", produto.to_json_catalogo() )   
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro ao cadastrar", "produto", {})

#Atualizar os dados de um produto
@app.route("/catalogo/<id>", methods=["PUT"])
@auth.login_required
def atualiza_produto(id):
    produto_objeto = Catalogo.query.filter_by(id=id).first()
    body = request.get_json()
 
    try:
        if body["disponibilidade"] == False and produto_objeto.disponibilidade == True:
            response = requests.delete(URL_inventario+"produto/"+str(produto_objeto.id), auth=(user, senha))
        if('nome' in body):
            produto_objeto.nome = body["nome"]
        if('descricao' in body):
            produto_objeto.descricao = body["descricao"]
        if('preco' in body):
            produto_objeto.preco = body["preco"]
        if('disponibilidade' in body):
            produto_objeto.disponibilidade = body["disponibilidade"]
 
        db.session.add(produto_objeto)
        db.session.commit()    
        return geraResponse(200, "Atualizado com sucesso", "produto", produto_objeto.to_json_catalogo())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao atualizar", "produto", {})

#Deletar um produto pelo ID
@app.route("/catalogo/<id>", methods=["DELETE"])
@auth.login_required
def deleta_produto(id):
    produto_objeto = db.session.query(Catalogo).get(id)
    try: 
        produto_objeto.disponibilidade = 0
        db.session.add(produto_objeto)
        db.session.commit()
        return geraResponse(200, "Deletado com sucesso", "produto", produto_objeto.to_json_catalogo())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao deletar", "produto", {}) 