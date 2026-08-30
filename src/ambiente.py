import random

class Ambiente:
    def __init__(self, linhas, colunas):
        # "linhas" e "colunas" representam a AREA UTIL do ambiente (onde
        # obstaculos, sujeiras e o robo sao sorteados). A matriz real tem
        # 2 linhas e 2 colunas a mais, porque nasce cercada por uma
        # moldura de obstaculos (paredes) em toda a borda externa.
        self.linhas = linhas
        self.colunas = colunas

        self.matriz = [[1] * (colunas + 2) for _ in range(linhas + 2)]
        for l in range(1, linhas + 1):
            for c in range(1, colunas + 1):
                self.matriz[l][c] = 0

        total = linhas * colunas
        self.quantidade_obstaculos = int(total * 0.2)
        self.quantidade_sujeiras = int(total * 0.1)
        self.posicao_robo = None

    def gerar_ambiente(self):
        total = self.linhas * self.colunas

        quantidade_posicoes = (
            self.quantidade_obstaculos
            + self.quantidade_sujeiras
            + 1
        )

        sorteados = random.sample(range(total), quantidade_posicoes)

        inicio_sujeiras = self.quantidade_obstaculos
        fim_sujeiras = inicio_sujeiras + self.quantidade_sujeiras

        obstaculos = sorteados[:inicio_sujeiras]
        sujeiras = sorteados[inicio_sujeiras:fim_sujeiras]
        robo = sorteados[-1]

        # todas as posicoes sorteadas sao relativas a AREA UTIL (0-indexada
        # sem a moldura); por isso somamos +1 ao gravar na matriz real, que
        # tem a moldura ocupando a linha/coluna 0.
        for posicao in obstaculos:
            linha = posicao // self.colunas
            coluna = posicao % self.colunas
            self.matriz[linha + 1][coluna + 1] = 1

        for posicao in sujeiras:
            linha = posicao // self.colunas
            coluna = posicao % self.colunas
            self.matriz[linha + 1][coluna + 1] = 2

        linha_robo = robo // self.colunas
        coluna_robo = robo % self.colunas
        # posicao_robo fica em coordenadas da AREA UTIL (sem moldura), para
        # o resto do sistema continuar tratando (0,0) como o canto real do
        # ambiente, independente de como a matriz interna esta organizada.
        self.posicao_robo = (linha_robo, coluna_robo)
        self.matriz[linha_robo + 1][coluna_robo + 1] = 3

    def mostrar_matriz(self):
        for linha in self.matriz:
            print(linha)