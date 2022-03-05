from dotenv import load_dotenv
load_dotenv() 
from models.papel import Papel
from models.user import User


dados_user = User(
    nome = 'Matheus Ayron',
    email= 'matheus@gmail.com',
    senha= '123456',
    cpf= '8888888',
    saldo_atual = 5000
)

#dados_user.cadastrar()
#user  = User.from_cpf('8888888')

#papel = Papel('AERI3')
#user.comprar(papel, 10)

historico = User.get_historico('8888888')

print(historico)