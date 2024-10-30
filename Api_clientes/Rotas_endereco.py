from Main import *
from Gateway import *

# Seleciona todos endereços
@app.route("/enderecos", methods=["GET"])
@auth.login_required
def seleciona_enderecos():
    try:
        enderecos_objeto = db.session.query(Enderecos).filter(Enderecos.ativo == 1).all()
        enderecos_json = [endereco.to_json_endereco_ativo() for endereco in enderecos_objeto]
        return geraResponse(200, "ok", "enderecos", enderecos_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "endereco", {})

#Seleciona Individualmente um endereço pelo ID, além dos dados do cliente associado ao endereço
@app.route("/enderecos/<id>", methods=["GET"])
@auth.login_required
def seleciona_endereco(id):
    try:
        endereco_objeto = db.session.query(Enderecos).filter(Enderecos.id == id, Enderecos.ativo == 1).first()
        endereco_json = endereco_objeto.to_json_endereco_ativo()
        cliente_endereco_objeto = endereco_objeto.dono
        cliente_endereco_json = cliente_endereco_objeto.to_json()
        return geraResponse(200, "ok", "endereco", endereco_json, "cliente", cliente_endereco_json)
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro na consulta", "endereco", {})

#Cadastrar um novo endereço
@app.route("/enderecos", methods=["POST"])
@auth.login_required    
def cadastra_endereco():

    body = request.get_json()  
    try:
        endereco = Enderecos(id_cliente = body["id_cliente"],rua = body["rua"], numero = body["numero"], complemento = body["complemento"], CEP = body["CEP"], ativo = True)
        db.session.add(endereco)
        db.session.commit()
        return geraResponse(201, "Cadastrado com sucesso", "endereco", endereco.to_json_endereco())   
    except Exception as e:
        print(e)
        return geraResponse(400, "Erro ao cadastrar", "endereco", {})

#Atualizar os dados de um endereço
@app.route("/enderecos/<id>", methods=["PUT"])
@auth.login_required
def atualiza_endereco(id):
    endereco_objeto = db.session.query(Enderecos).get(id)
    body = request.get_json()
 
    try:
        if('id_cliente' in body):
            endereco_objeto.id_cliente = body["id_cliente"]
        if('rua' in body):
            endereco_objeto.rua = body["rua"]
        if('numero' in body):
            endereco_objeto.numero = body["numero"]
        if('complemento' in body):
            endereco_objeto.complemento = body["complemento"]
        if('CEP' in body):
            endereco_objeto.CEP = body["CEP"]
 
        db.session.add(endereco_objeto)
        db.session.commit()    
        return geraResponse(200, "Atualizado com sucesso", "endereco", endereco_objeto.to_json_endereco())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao atualizar", "endereco", {})

#Deletar um endereço pelo ID
@app.route("/enderecos/<id>", methods=["DELETE"])
@auth.login_required
def deleta_endereco(id):
    endereco_objeto = db.session.query(Enderecos).get(id)
    try:
        endereco_objeto.ativo = 0
        db.session.commit()    
        return geraResponse(200, "Deletado com sucesso", "endereco", endereco_objeto.to_json_endereco())
 
    except Exception as e:
        print("Erro", e)
        return geraResponse(400, "Erro ao deletar", "endereco", {}) 


