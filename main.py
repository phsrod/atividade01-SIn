from ambiente import Ambiente
from robo_dfs import robo_limpeza, visitados
from visualizador import animar_limpeza

def main():
    linhas = 10
    colunas = 10
    intervalo = 0.2

    ambiente = Ambiente(linhas, colunas)

    ambiente.gerar_ambiente()

    matriz_trabalho = []
    for linha in ambiente.matriz:
        matriz_trabalho.append(linha[:])

    linha_robo, coluna_robo = ambiente.posicao_robo

    robo_limpeza(matriz_trabalho, linha_robo, coluna_robo, linhas, colunas)

    animar_limpeza(ambiente, visitados, intervalo)


if __name__ == "__main__":
    main()