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
        self.matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.quantidade_obstaculos = int(linhas * colunas * 0.2)
        self.quantidade_sujeiras = int(linhas * colunas * 0.1)
        self.posicao_robo = None

    def gerar_ambiente(self):
        posicoes = [(linha, coluna) for linha in range(self.linhas) for coluna in range(self.colunas)
        ]

        posicoes_obstaculos = random.sample(
            posicoes,
            self.quantidade_obstaculos
        )

        for linha, coluna in posicoes_obstaculos:
            self.matriz[linha][coluna] = 1

        posicoes_livres = [posicao for posicao in posicoes if posicao not in posicoes_obstaculos]

        posicoes_sujeira = random.sample(posicoes_livres, self.quantidade_sujeiras)

        for linha, coluna in posicoes_sujeira:
            self.matriz[linha][coluna] = 2

        posicoes_livres = [posicao for posicao in posicoes_livres if posicao not in posicoes_sujeira]

        self.posicao_robo = random.choice(posicoes_livres)

        linha, coluna = self.posicao_robo
        self.matriz[linha][coluna] = 3

    def mostrar_matriz(self):

        for linha in self.matriz:
            print(linha)

