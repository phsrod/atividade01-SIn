# convencao:
# 0 = espaço livre
# 1 = obstáculo
# 2 = sujeira
# 3 = robô

import random

class Ambiente:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = []

        for i in range(linhas):
            linha = []
            for j in range(colunas):
                linha.append(0)
            self.matriz.append(linha)

        self.quantidade_obstaculos = int(linhas * colunas * 0.2)
        self.quantidade_sujeiras = int(linhas * colunas * 0.1)
        self.posicao_robo = None

    def gerar_ambiente(self):
        posicoes = []

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                posicoes.append((linha, coluna))

        obstaculos = random.sample(posicoes, self.quantidade_obstaculos)

        for linha, coluna in obstaculos:
            self.matriz[linha][coluna] = 1

        posicoes_livres = []

        for posicao in posicoes:
            if posicao not in obstaculos:
                posicoes_livres.append(posicao)

        sujeiras = random.sample(posicoes_livres, self.quantidade_sujeiras)

        for linha, coluna in sujeiras:
            self.matriz[linha][coluna] = 2

        novas_posicoes_livres = []

        for posicao in posicoes_livres:
            if posicao not in sujeiras:
                novas_posicoes_livres.append(posicao)

        posicoes_livres = novas_posicoes_livres

        self.posicao_robo = random.choice(posicoes_livres)

        linha, coluna = self.posicao_robo
        self.matriz[linha][coluna] = 3

    def mostrar_matriz(self):
        for linha in self.matriz:
            print(linha)
            

