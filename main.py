from models.papel import PapelAcao
from models.user import User
from dotenv import load_dotenv



load_dotenv() 


dados_user = User(
    nome = 'Matheus Ayron',
    email= 'gg@gmail.com',
    senha= '123456',
    cpf= '44444',
    patrimonio= 450.3
)


dados_user.cadastrar()


#print(dados_user.nome)