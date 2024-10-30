from Main import *
from Rotas_endereco import *
from Rotas_cliente import *
from Gateway import *

db.create_all()

#Executa o aplicativo criado no Main.py
app.run(host='0.0.0.0', port=5000)