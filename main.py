from dotenv import load_dotenv
load_dotenv() 
from models.papel import Papel
from models.user import User


user  = User.from_cpf('44444')
papel = Papel('OIBR3')

print(user)

#user.comprar(papel, 10)

print(user)

