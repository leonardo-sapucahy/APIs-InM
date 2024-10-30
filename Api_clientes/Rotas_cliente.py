from Main import *
from Gateway import *
import requests

#Define a rota da home
@app.route("/", methods=["GET"])
@auth.login_required
def Inicial():
    return "Olá, {}!".format(auth.current_user())

# Seleciona todos os clientes
@app.route("/clientes", methods=["GET"])
@auth.login_required
def seleciona_clientes():
    clientes_enderecos = []
    try:
        clientes_objeto = db.session.query(Clientes).filter(Clientes.ativo == 1).all()
        for cliente in clientes_objeto:
            enderecos_objeto = db.session.query(Enderecos).filter(Enderecos.id_cliente == cliente.id, Enderecos.ativo == 1).all()
            clientes_enderecos.append(cliente.to_json_ativo())
            for endereco in enderecos_objeto:
                clientes_enderecos.append(endereco.to_json_endereco_ativo())
        return geraResponse(200, "ok", "clientes", clientes_enderecos)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "clientes", {})

#Seleciona Individualmente um cliente pelo ID
@app.route("/clientes/<id>", methods=["GET"])
@auth.login_required
def seleciona_cliente(id):
    try:
        cliente_objeto = db.session.query(Clientes).filter(Clientes.id == id, Clientes.ativo == 1).first()
        cliente_json = cliente_objeto.to_json_ativo()
        return geraResponse(200, "ok", "cliente", cliente_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "cliente", {})

#Cadastrar novo cliente
@app.route("/clientes", methods=["POST"])    
@auth.login_required
def cadastra_cliente():

    body = request.get_json()  
    try:
        cliente = Clientes(nome = body["nome"], cpf = body["cpf"], email = body["email"], senha = body["senha"], ativo = 1)
        cliente_ja_cadastrado = db.session.query(Clientes).filter(Clientes.cpf == body["cpf"], Clientes.ativo == 0).first()
        if cliente_ja_cadastrado != None:
            cliente_ja_cadastrado.senha = body["senha"]
            cliente_ja_cadastrado.ativo = 1
            cliente = cliente_ja_cadastrado
        db.session.add(cliente)
        cliente_id = db.session.query(Clientes).filter(Clientes.cpf == body["cpf"]).first()
        endereco = Enderecos(id_cliente = cliente_id.id,rua = body["rua"], numero = body["numero"], complemento = body["complemento"], CEP = body["CEP"], ativo = True)
        db.session.add(endereco)
        db.session.commit()
        return geraResponse(201, "Cadastrado com sucesso", "cliente", cliente.to_json_ativo() )   
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro ao cadastrar", "cliente", {})

#Atualizar os dados de um cliente pelo ID
@app.route("/clientes/<id>", methods=["PUT"])
@auth.login_required
def atualiza_cliente(id):
    cliente_objeto = db.session.query(Clientes).get(id)
    body = request.get_json()
 
    try:
        if('nome' in body):
            cliente_objeto.nome = body["nome"]
        if('cpf' in body):
            cliente_objeto.cpf = body["cpf"]
        if('email' in body):
            cliente_objeto.email = body["email"]
        if('senha' in body):
            cliente_objeto.senha = body["senha"]
 
        db.session.add(cliente_objeto)
        db.session.commit()    
        return geraResponse(200, "Atualizado com sucesso", "cliente", cliente_objeto.to_json_ativo())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao atualizar", "cliente", {})

#Deleta um cliente pelo ID, seu(s) enderecos e sua(s) compra(s) no inventario
@app.route("/clientes/<id>", methods=["DELETE"])
@auth.login_required
def deleta_cliente(id):
    cliente_objeto = db.session.query(Clientes).get(id)
    endereco_cliente_objeto = cliente_objeto.casa
    try:
        requests.delete('http://127.0.0.1:5002/inventario/cliente/'+id, auth=(user, senha))
        cliente_objeto.ativo = 0
        db.session.add(cliente_objeto)
        for endereco in endereco_cliente_objeto:
            endereco.ativo = 0 
            db.session.add(endereco)
        db.session.commit() 
        return geraResponse(200, "Deletado com sucesso", "cliente", cliente_objeto.to_json_ativo())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao deletar", "cliente", {}) 

