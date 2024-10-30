from Main import *
from Gateway import *
import requests

URL_catalogo = 'http://127.0.0.1:5001/catalogo/'
URL_cliente = 'http://127.0.0.1:5000/clientes/'

#Define a rota da home
@app.route("/", methods=["GET"])
@auth.login_required
def Inicial():
    return "Olá, {}!".format(auth.current_user())

# Seleciona todos os inventarios com as informações dos produtos e clientes
@app.route("/inventario", methods=["GET"])
@auth.login_required
def seleciona_inventarios_cliente_produto():
    cliente_produto = []
    try:
        inventarios_objeto = db.session.query(Inventario).all()
        for inventario in inventarios_objeto:
            response_cliente = requests.get(URL_cliente+str(inventario.id_cliente), auth=(user, senha))
            response_produto = requests.get(URL_catalogo+str(inventario.id_produto), auth=(user, senha))
            if response_cliente.status_code == 200 and response_produto.status_code == 200:
                cliente_produto.append(response_cliente)
                cliente_produto.append(response_produto)
        inventarios_json = [inventario.json() for inventario in cliente_produto]
        return geraResponse(200, "ok", "inventario", inventarios_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "inventario", {})

# Seleciona todos os inventarios
@app.route("/inventario/id", methods=["GET"])
@auth.login_required
def seleciona_catalogo_id():
    try:
        inventario_objeto = db.session.query(Inventario).all()
        inventario_json = [inventario.to_json_inventario() for inventario in inventario_objeto]
        return geraResponse(200, "ok", "inventario", inventario_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "inventario", {})

#Seleciona um cliente pelo ID e seus produtos
@app.route("/inventario/cliente/<id>", methods=["GET"])
@auth.login_required
def seleciona_inventario_cliente(id):
    produtos_response = []
    try:
        response = requests.get(URL_cliente+id, auth=(user, senha))
        if response.status_code == 200:
            response_json = response.json()
            id_produtos = db.session.query(Inventario).filter(Inventario.id_cliente == id).all() 
            for produto in id_produtos:
                response = requests.get(URL_catalogo+str(produto.id_produto), auth=(user, senha))
                if response.status_code == 200:
                    produtos_response.append(response)
            response_json_produtos = [produto_objeto.json() for produto_objeto in produtos_response]
        else:
            return geraResponse(400, "Cliente não encontrado", "cliente", {})

        return geraResponse(200, "ok", "cliente", response_json, "produtos", response_json_produtos)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "inventario", {})

#Seleciona um produto pelo ID e seus compradores
@app.route("/inventario/produto/<id>", methods=["GET"])
@auth.login_required
def seleciona_inventario_produto(id):
    clientes_response = []
    try:
        response = requests.get(URL_catalogo+id, auth=(user, senha))
        if response.status_code == 200:
            response_json = response.json()
            id_clientes = db.session.query(Inventario).filter(Inventario.id_produto == id).all() 
            for cliente in id_clientes:
                response = requests.get(URL_cliente+str(cliente.id_cliente), auth=(user, senha))
                if response.status_code == 200:
                    clientes_response.append(response)
            response_json_clientes = [cliente_obejto.json() for cliente_obejto in clientes_response]
        else:
            return geraResponse(400, "Produto não encontrado", "produto", {})

        return geraResponse(200, "ok", "produto", response_json, "clientes", response_json_clientes)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "inventario", {})

#Cadastrar uma compra de produto
@app.route("/inventario", methods=["POST"])
@auth.login_required    
def cadastra_compra():
    body = request.get_json()
    try:
        compra_ja_existe = db.session.query(Inventario).filter(Inventario.id_cliente == body["id_cliente"], Inventario.id_produto == body["id_produto"]).first()
        if compra_ja_existe == None:
            inventario = Inventario(id_cliente = body["id_cliente"], id_produto = body["id_produto"])
            response_produto = requests.get(URL_catalogo+inventario.id_produto, auth=(user, senha))
            response_cliente = requests.get(URL_cliente+inventario.id_cliente, auth=(user, senha))
            if response_cliente.status_code == 400 or response_produto.status_code == 400:
                return geraResponse(400, "Cliente ou produto inexistente", "compra", {})
        else:
            return geraResponse(400, "Compra já realizada", "id:"+str(compra_ja_existe.id), {})
        db.session.add(inventario)
        db.session.commit()
        return geraResponse(201, "Compra realizada com sucesso", "compra", inventario.to_json_inventario())   
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro ao comprar", "compra", {})

#Atualizar os dados de uma compra
@app.route("/inventario/<id>", methods=["PUT"])
@auth.login_required
def atualiza_compra(id):
    inventario_objeto = db.session.query(Inventario).get(id)
    body = request.get_json()

    try:
        if requests.get(URL_cliente+body["id_cliente"], auth=(user, senha)).status_code == 400 or requests.get(URL_catalogo+body["id_produto"], auth=(user, senha)).status_code == 400:
            return geraResponse(400, "Cliente ou produto inexistente", "Compra", {})
        if('id_cliente' in body):
            inventario_objeto.id_cliente = body["id_cliente"]
        if('id_produto' in body):
            inventario_objeto.id_produto = body["id_produto"]
 
        db.session.add(inventario_objeto)
        db.session.commit()    
        return geraResponse(200, "Atualizado com sucesso", "compra", inventario_objeto.to_json_inventario())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao atualizar", "compra", {})

#Deletar um inventario pelo ID
@app.route("/inventario/<id>", methods=["DELETE"])
@auth.login_required
def deleta_compra(id):
    inventario_objeto = db.session.query(Inventario).get(id)
    try:
        db.session.delete(inventario_objeto)
        db.session.commit()    
        return geraResponse(200, "Deletado com sucesso", "compra", inventario_objeto.to_json_inventario())
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao deletar", "compra", {}) 

# Deleta um inventario pelo id do cliente
@app.route("/inventario/cliente/<id>", methods=["DELETE"])
@auth.login_required
def deleta_cliente_inventarios(id):
    try:
        inventarios_objeto = db.session.query(Inventario).filter(Inventario.id_cliente == id).all()
        for inventario in inventarios_objeto:
            db.session.delete(inventario)
        db.session.commit()
        return geraResponse(200, "Deletado com sucesso", " ", {})
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro ao deletar", "inventario", {})

# Deleta um inventario pelo id do produto
@app.route("/inventario/produto/<id>", methods=["DELETE"])
@auth.login_required
def deleta_produto_inventarios(id):
    try:
        inventarios_objeto = db.session.query(Inventario).filter(Inventario.id_produto == id).all()
        for inventario in inventarios_objeto:
            db.session.delete(inventario)
        db.session.commit()
        return geraResponse(200, "Deletado com sucesso", " ", {})
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro ao deletar", "inventario", {})

    