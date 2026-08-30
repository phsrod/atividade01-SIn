from ambiente import Ambiente
from robo_dfs import robo_limpeza_dfs, SensorAmbiente
from visualizador import plotar_ambiente, animar_limpeza


def main():
    linhas = 1000
    colunas = 1000
    intervalo = 0.0001
    opcao = 2
    ambiente = Ambiente(linhas, colunas)

    ambiente.gerar_ambiente()

    if opcao == 1:
        plotar_ambiente(ambiente)

    elif opcao == 2:
        linha_robo, coluna_robo = ambiente.posicao_robo

        # total de sujeiras no ambiente ORIGINAL — essa matriz não é mais
        # alterada pelo robô (ele limpa numa cópia de trabalho própria,
        # guardada dentro do SensorAmbiente), justamente para o
        # visualizador poder animar a limpeza célula a célula a partir do
        # estado original.
        total_sujeiras = sum(linha.count(2) for linha in ambiente.matriz)

        # O robô nunca recebe "ambiente" nem a matriz. Ele recebe apenas um
        # SensorAmbiente — um objeto que só sabe responder "o que existe
        # ao redor dessa posição?" e "limpa essa posição se estiver suja".
        # A matriz completa fica guardada dentro do sensor, fora do
        # alcance da lógica de decisão do robô.
        sensor = SensorAmbiente(ambiente)
        caminho, sujeiras_limpas, mapa_mental = robo_limpeza_dfs(
            sensor, linha_robo, coluna_robo
        )

        print(f"Sujeiras limpas: {sujeiras_limpas}/{total_sujeiras}")
        print(f"Passos totais (com recuos): {len(caminho)}")

        animar_limpeza(ambiente, caminho, intervalo)

    else:
        print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()