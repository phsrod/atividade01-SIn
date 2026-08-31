import random

DIRECOES = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}


class Ambiente:
    def __init__(self, linhas, colunas):
        # "linhas" e "colunas" representam a AREA UTIL do ambiente (onde obstaculos, sujeiras e o robo sao sorteados). A matriz real tem 2 linhas e 2 colunas a mais, porque nasce cercada por uma moldura de obstaculos (paredes) em toda a borda externa.
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

        quantidade_posicoes = (self.quantidade_obstaculos + self.quantidade_sujeiras + 1)

        sorteados = random.sample(range(total), quantidade_posicoes)

        inicio_sujeiras = self.quantidade_obstaculos
        fim_sujeiras = inicio_sujeiras + self.quantidade_sujeiras

        obstaculos = sorteados[:inicio_sujeiras]
        sujeiras = sorteados[inicio_sujeiras:fim_sujeiras]
        robo = sorteados[-1]

        # todas as posicoes sorteadas sao relativas a AREA UTIL (0-indexada sem a moldura); por isso somamos +1 ao gravar na matriz real, que tem a moldura ocupando a linha/coluna 0.
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
        # posicao_robo fica em coordenadas da AREA UTIL (sem moldura), para o resto do sistema continuar tratando (0,0) como o canto real do ambiente, independente de como a matriz interna esta organizada.
        self.posicao_robo = (linha_robo, coluna_robo)
        self.matriz[linha_robo + 1][coluna_robo + 1] = 3

        # Estado usado durante a execução. A matriz original é preservada
        # para que o visualizador possa animar a limpeza posteriormente.
        self._matriz_trabalho = [linha[:] for linha in self.matriz]
        self._linha_robo = linha_robo + 1
        self._coluna_robo = coluna_robo + 1
        self._caminho_real = [self.posicao_robo]

    def sentir_arredores(self):
        """Retorna apenas o conteúdo das quatro células adjacentes."""
        percepcoes = {}
        for nome, (dl, dc) in DIRECOES.items():
            valor = self._matriz_trabalho[self._linha_robo + dl][self._coluna_robo + dc]
            if valor == 1:
                percepcoes[nome] = "obstaculo"
            elif valor == 2:
                percepcoes[nome] = "sujeira"
            else:
                percepcoes[nome] = "livre"
        return percepcoes

    def mover_robo(self, direcao):
        """Executa um movimento físico, se a direção não estiver bloqueada."""
        dl, dc = DIRECOES[direcao]
        nova_linha = self._linha_robo + dl
        nova_coluna = self._coluna_robo + dc
        if self._matriz_trabalho[nova_linha][nova_coluna] == 1:
            return False

        self._linha_robo = nova_linha
        self._coluna_robo = nova_coluna
        self._caminho_real.append((nova_linha - 1, nova_coluna - 1))
        return True

    def limpar_posicao_robo(self):
        """Limpa a célula onde o robô está, se houver sujeira."""
        if self._matriz_trabalho[self._linha_robo][self._coluna_robo] == 2:
            self._matriz_trabalho[self._linha_robo][self._coluna_robo] = 0
            return True
        return False

    def caminho_real(self):
        """Registro do ambiente para uso exclusivo da visualização."""
        return self._caminho_real[:]

    def mostrar_matriz(self):
        for linha in self.matriz:
            print(linha)
