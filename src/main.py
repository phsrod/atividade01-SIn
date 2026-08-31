from ambiente import Ambiente
from robo_dfs import robo_limpeza_dfs, SensorAmbiente
from visualizador import plotar_ambiente, animar_limpeza


def main():
    linhas = 20
    colunas = 20
    intervalo = 0.0001
    opcao = 2
    ambiente = Ambiente(linhas, colunas)

    ambiente.gerar_ambiente()

    if opcao == 1:
        plotar_ambiente(ambiente)

    elif opcao == 2:
        # A matriz original é preservada pelo Ambiente para a animação; ele
        # mantém internamente outra matriz para executar os movimentos.
        total_sujeiras = sum(linha.count(2) for linha in ambiente.matriz)

        # O DFS recebe apenas o sensor. O Ambiente continua dono da matriz e
        # da posição absoluta do robô.
        sensor = SensorAmbiente(ambiente)
        sujeiras_limpas, mapa_mental = robo_limpeza_dfs(sensor)
        caminho = ambiente.caminho_real()

        print(f"Sujeiras limpas: {sujeiras_limpas}/{total_sujeiras}")
        print(f"Passos totais (com recuos): {len(caminho)}")

        animar_limpeza(ambiente, caminho, intervalo)

    else:
        print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
