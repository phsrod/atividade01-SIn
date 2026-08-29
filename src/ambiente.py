import random

class Ambiente:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = [[0] * colunas for _ in range(linhas)]

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
        robo = sorteados[-1]  # <- agora essa variável é de fato usada

        for posicao in obstaculos:
            linha = posicao // self.colunas
            coluna = posicao % self.colunas
            self.matriz[linha][coluna] = 1

        for posicao in sujeiras:
            linha = posicao // self.colunas
            coluna = posicao % self.colunas
            self.matriz[linha][coluna] = 2

        # Agora usamos a variável 'robo' para definir a posição do robô
        linha_robo = robo // self.colunas
        coluna_robo = robo % self.colunas
        self.posicao_robo = (linha_robo, coluna_robo)
        self.matriz[linha_robo][coluna_robo] = 3

    def mostrar_matriz(self):
        for linha in self.matriz:
            print(linha)