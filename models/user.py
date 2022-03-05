from pydantic import BaseModel
import database
import bcrypt
import pymongo
from models.papel import Papel, PapelEmCarteira
from models.exceptions import SaldoInsuficiente
from datetime import datetime


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
        
        self.senha = bcrypt.hashpw(self.senha.encode('utf-8'), bcrypt.gensalt())

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

        for i in self.carteira:
            if i.codigo_papel == papel.codigo_papel:
                i.qtd         +=  qtd
                break
        else:                                                                                   #Caso não tenha um break
            self.carteira.append(PapelEmCarteira(codigo_papel = papel.codigo_papel, qtd = qtd)) #Append acrescenta o valor


        database.client.corretora_ayron.user.update_one(
            {'cpf': self.cpf}, 
            { "$set": {
                'saldo_atual': self.saldo_atual,
                'carteira':    [i.dict() for i in self.carteira ]   #para todos os iens na minha carteira eu tranformo para um dicionario, pq o mongo não sabe como salvar no banco
            }}
        )

        # adicionar essa transação ao historico

        database.client.corretora_ayron.historico.insert_one({
            'cpf_user': self.cpf,
            'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'papel': {
                'codigo': papel.codigo_papel,
                'qtd': qtd,
                'valor_unitario': papel.preco_atual,
                'valor_total': papel.preco_atual * qtd
            },
            'qtd_total_carteira_apos_operacao': i.qtd,
            'operacao': 'compra'
        })


    def get_historico(cpf: str):
        result_historico = database.client.corretora_ayron.historico.find_one({'cpf_user':cpf })

        return result_historico


#criar função get historico, e retornar pra nois todo o historico

#Como eu pegaria somente a qtd total da ação apos a compra ou venda?