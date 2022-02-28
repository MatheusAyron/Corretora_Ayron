from dotenv import load_dotenv
load_dotenv() 
from models.papel import Papel
from models.user import User


""" dados_user = User(
    nome = 'Matheus Ayron',
    email= 'ttt@gmail.com',
    senha= '123456',
    cpf= '8888888',
    patrimonio= 450.3
) """

#dados_user.cadastrar()
user  = User.from_cpf('44444')
papel = Papel('AERI3')

user.comprar(papel, 10)

print(user)