from ambiente import Ambiente
from robo_dfs import robo_limpeza_dfs
from visualizador import plotar_ambiente, animar_limpeza


def main():
    linhas = 1000
    colunas = 1000
    intervalo = 0.0001  # intervalo de tempo entre os passos da animação (em segundos)
    opcao = 2
    ambiente = Ambiente(linhas, colunas)

    ambiente.gerar_ambiente()

    if opcao == 1:
        plotar_ambiente(ambiente)

    elif opcao == 2:
        linha_robo, coluna_robo = ambiente.posicao_robo

        # total de sujeiras no ambiente ORIGINAL — essa matriz não é mais
        # alterada pelo robô (ele limpa numa cópia de trabalho própria),
        # justamente para o visualizador poder animar a limpeza célula a
        # célula a partir do estado original.
        total_sujeiras = sum(linha.count(2) for linha in ambiente.matriz)

        # O robô só recebe o AMBIENTE (para o sensor poder consultar as
        # células ao redor da posição real) e a posição inicial real —
        # tudo o que ele decide depois disso é baseado no que sente e no
        # mapa mental que ele mesmo constrói, nunca em acesso direto e
        # completo à matriz.
        caminho, sujeiras_limpas, mapa_mental = robo_limpeza_dfs(
            ambiente, linha_robo, coluna_robo
        )

        print(f"Sujeiras limpas: {sujeiras_limpas}/{total_sujeiras}")
        print(f"Passos totais (com recuos): {len(caminho)}")

        animar_limpeza(ambiente, caminho, intervalo)

    else:
        print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()