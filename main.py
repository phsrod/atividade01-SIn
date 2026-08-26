import sys
sys.setrecursionlimit(2_000_000)

from ambiente import Ambiente
from robo_dfs import robo_limpeza, visitados
from visualizador import plotar_ambiente, animar_limpeza

def main():
    linhas = 1000
    colunas = 1000
    intervalo = 0.1
    opcao = 2
    ambiente = Ambiente(linhas, colunas)

    ambiente.gerar_ambiente()

    if opcao == 1:
        plotar_ambiente(ambiente)

    elif opcao == 2:
        matriz_trabalho = []
        for linha in ambiente.matriz:
            matriz_trabalho.append(linha[:])

        linha_robo, coluna_robo = ambiente.posicao_robo

        robo_limpeza(matriz_trabalho, linha_robo, coluna_robo, linhas, colunas)

        animar_limpeza(ambiente, visitados, intervalo)

    else:
        print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()