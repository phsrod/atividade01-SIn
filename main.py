from ambiente import Ambiente
from visualizador import plotar_ambiente


def main():
    linhas = 10
    colunas = 10

    ambiente = Ambiente(linhas, colunas)

    ambiente.gerar_ambiente()

    plotar_ambiente(ambiente)


if __name__ == "__main__":
    main()