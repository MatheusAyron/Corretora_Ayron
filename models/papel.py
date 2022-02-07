import requests

class PapelAcao:

    _ACAOAVAILABLE: list = requests.get('https://brapi.ga/api/available').json()['stocks']
    
    def __init__(self, codigo_acao: str):
        ''' Construtor recebe código da ação negociada na B3 '''
        self.codigo_acao = codigo_acao.upper()

        if not self.codigo_acao in PapelAcao._ACAOAVAILABLE:
            raise ValueError(f'Ação = {self.codigo_acao} inválida')

        self.atualizar()
    

    def __repr__(self):
        ''' Representção de return bem sucedido '''
        return f'<PapelAcao {self.codigo_acao} válida>'


    def atualizar(self):
        ''' Busca e atualiza os indicadores da ação '''
        response = requests.get(f'https://brapi.ga/api/quote/{self.codigo_acao}?interval=1d&range=1y')

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
