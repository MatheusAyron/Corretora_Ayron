from pydantic import BaseModel
import requests

class PapelEmCarteira(BaseModel):
    codigo_papel: str
    qtd: int


class Papel:

    _ACAOAVAILABLE: list = requests.get('https://brapi.ga/api/available').json()['stocks']
    
    def __init__(self, codigo_papel: str):
        ''' Construtor recebe código da ação negociada na B3 '''
        self.codigo_papel = codigo_papel.upper()

        if not self.codigo_papel in Papel._ACAOAVAILABLE:
            raise ValueError(f'Ação = {self.codigo_papel} inválida')

        self.atualizar()
    

    def __repr__(self):
        ''' Representção de return bem sucedido '''
        return f'<Papel {self.codigo_papel} válida>'


    def atualizar(self):
        ''' Busca e atualiza os indicadores da ação '''
        response = requests.get(f'https://brapi.ga/api/quote/{self.codigo_papel}?interval=1d&range=1y')

        if response.status_code != 200:
            raise Exception('Erro ao fazer requisição na API')

        data = response.json()['results'][0]

        self.preco_atual              = data['regularMarketPrice']
        self.maxima_dia               = data['regularMarketDayHigh']
        self.minima_dia               = data['regularMarketDayLow']
        self.valorizacao_dia          = data['regularMarketChangePercent']
        self.volume_dia               = data['regularMarketVolume']
        self.minima_cinquenta_semana  = data['fiftyTwoWeekLow']
        self.maxima_cinquenta_semana  = data['fiftyTwoWeekHigh']
        self.dados_historicos         = data['historicalDataPrice']
