from pydantic import BaseModel
import database
import bcrypt
import pymongo
from models.papel import Papel, PapelEmCarteira
from models.exceptions import SaldoInsuficiente


class User(BaseModel):
    ''' Dados do usuario '''
    nome: str
    email: str
    senha: str
    cpf: str
    patrimonio: float               = 0
    saldo_atual: float              = 0
    carteira: list[PapelEmCarteira] = [] 


    @classmethod
    def from_cpf(cls, cpf: str):
        result = database.client.corretora_ayron.user.find_one({'cpf': cpf})
        user   = User(**result)

        return user

    def cadastrar(self):
        """ Insere o usúario no banco de dados, tabela user, e valida se o CPF ou Email ja existem """
        
        try: 
            result = database.client.corretora_ayron.user.insert_one(self.dict())
        except pymongo.errors.DuplicateKeyError as e:
            raise ValueError from e

        return result

    def comprar(self, papel: Papel, qtd: int):
        if (papel.preco_atual * qtd) > self.saldo_atual:
            raise SaldoInsuficiente()
        
        self.saldo_atual -= papel.preco_atual * qtd

        # se existir esse papel na carteira, atualiza o valor
        #   self.carteira = 
        # se não existir, cria esse elemento na carteira com a qtd atual/inicial
        #   self.carteira = 
        
        database.client.corretora_ayron.user.update_one(
            {'cpf': self.cpf}, 
            {
                'saldo_atual': self.saldo_atual,
                'carteira':    self.carteira
            }
        )

        # adicionar essa transação ao historico

        '''
            {
                'cpf_user': 'cpf',
                'data_hora': '2000-00-00 00:00:00',
                'papel': {
                    codigo: 'OIBR3',
                    qtd: 100,
                    valor_unitario: 0.5,
                    valor_total: 50,
                },
                'qtd_apos_operacao': 200,
                'operacao': 'VENDA', # ou COMPRA
            }
        '''
