from pydantic import BaseModel
import database



class User(BaseModel):
    '''  '''
    nome: str
    email: str
    senha: str
    cpf: str
    patrimonio: float   = 0
    saldo: float        = 0

    def cadastrar(self):
        ''' salva o User no banco de dados, se ja existir o usuario da erro. '''

        # cpf unico
        # email unico

        database.client 

''' User
{
    _id: "u01",
    nome: "dasdasdas"
}
'''

''' Historico
{
    _id: "t01",
    id_user: "u01",
    tran: {
        'pelpel': {
            codigo: 'oibr3'
            proço_atual: 9323.3123
        }
        'op': 'VENDA',
        'qtd': 312312,
    }
}

'''