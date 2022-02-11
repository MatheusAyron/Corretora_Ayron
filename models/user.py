from pydantic import BaseModel
import database
import bcrypt

class User(BaseModel):
    ''' Dados do usuario '''
    nome: str
    email: str
    senha: str
    cpf: str
    patrimonio: float   = 0
    saldo_atual: float  = 0

    def cadastrar(self):
        """ Insere o usúario no banco de dados, tabela user, e valida se o CPF ou Email ja existem """

        if database.client.corretora_ayron.user.find({'cpf': self.cpf}).count() > 0:
            raise ValueError('Registro CNPJ ja existente no banco, tabela user')
        elif database.client.corretora_ayron.user.find({'email': self.email}).count() > 0:
            raise ValueError('Registro EMAIL ja existente no banco, tabela user')
        
        database.client.corretora_ayron.user.insert(
            {
                'nome':         self.nome,
                'email':        self.email,
                'senha':        self.senha,
                'cpf':          self.cpf,
                'patrimonio' :  self.patrimonio,
                'saldo_atual':  self.saldo_atual
            }
        )



"""  def historico(self):

    database.client.corretora_ayron.historico.insert(
        {
            'cpf_user': database.client.corretora_ayron.user.find({'cpf': self.cpf}),
            'tran': {
                'papel': {
                    'codigo': PapelAcao.codigo_acao,
                    'preço_atual': self.preco_atual
                }
            }
        }
    ) """







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