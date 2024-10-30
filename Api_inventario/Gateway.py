from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from Main import *

#Cria a Basic Authentication
auth = HTTPBasicAuth()

#Define o usuario e senha
user = "admin"
senha = "senha"

#Define os usuários e senhas que poderão ser autenticados
sudo = {
    user: generate_password_hash(senha)    
}

#Função que verifica se a senha e usuário inseridos, conferem com a lista de usuáraios permitidos(sudo) 
@auth.verify_password
def verify_password(username, password):
    if username in sudo and \
            check_password_hash(sudo.get(username), password):
        return username
 

 