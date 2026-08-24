import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def calcular_tamanho_figura(ambiente):
    maior_dimensao = max(ambiente.linhas, ambiente.colunas)

    if maior_dimensao <= 20:
        escala = 0.45
    else:
        escala = 10 / maior_dimensao

    largura = max(4, ambiente.colunas * escala)
    altura = max(4, ambiente.linhas * escala)

    return largura, altura


def configurar_grade(ax, ambiente):
    if ambiente.linhas > 50 or ambiente.colunas > 50:
        ax.set_xticks([])
        ax.set_yticks([])
        return

    ax.set_xticks(range(ambiente.colunas))
    ax.set_yticks(range(ambiente.linhas))

    ax.set_xticks(
        [i - 0.5 for i in range(ambiente.colunas + 1)],
        minor=True
    )

    ax.set_yticks(
        [i - 0.5 for i in range(ambiente.linhas + 1)],
        minor=True
    )

    ax.grid(
        which="minor",
        color="black",
        linewidth=0.8
    )

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(which="both", length=0)
    ax.set_aspect("equal")


def criar_mapa_cores():
    return ListedColormap([
        "white",  # 0: espaço livre
        "black",  # 1: obstáculo
        "blue",   # 2: sujeira
        "red",    # 3: robô
    ])


def plotar_ambiente(ambiente):
    largura, altura = calcular_tamanho_figura(ambiente)
    cores = criar_mapa_cores()

    fig, ax = plt.subplots(figsize=(largura, altura))

    ax.imshow(
        ambiente.matriz,
        cmap=cores,
        vmin=0,
        vmax=3,
        interpolation="nearest",
        origin="upper"
    )

    configurar_grade(ax, ambiente)

    plt.tight_layout()
    plt.show()


def andar(posicao, restantes, caminho):
    linha, coluna = posicao

    vizinhos = [
        (linha + 1, coluna),
        (linha - 1, coluna),
        (linha, coluna + 1),
        (linha, coluna - 1),
    ]

    for vizinho in vizinhos:
        if vizinho in restantes:
            restantes.remove(vizinho)
            caminho.append(vizinho)

            andar(vizinho, restantes, caminho)

            caminho.append(posicao)


def gerar_caminho_continuo(visitados):
    if not visitados:
        return []

    restantes = set(visitados)
    primeira_posicao = visitados[0]

    restantes.remove(primeira_posicao)

    caminho = [primeira_posicao]
    andar(primeira_posicao, restantes, caminho)

    return caminho


def animar_limpeza(ambiente, caminho, intervalo=0.05):
    caminho = gerar_caminho_continuo(caminho)

    if not caminho:
        return

    largura, altura = calcular_tamanho_figura(ambiente)
    cores = criar_mapa_cores()

    matriz_visual = [
        linha[:]
        for linha in ambiente.matriz
    ]

    linha_robo, coluna_robo = ambiente.posicao_robo
    matriz_visual[linha_robo][coluna_robo] = 0

    fig, ax = plt.subplots(figsize=(largura, altura))

    imagem = ax.imshow(
        matriz_visual,
        cmap=cores,
        vmin=0,
        vmax=3,
        interpolation="nearest",
        origin="upper"
    )

    configurar_grade(ax, ambiente)

    robo, = ax.plot(
        coluna_robo,
        linha_robo,
        marker="o",
        markersize=6,
        color="red"
    )

    ax.set_title("Animação da limpeza")
    plt.tight_layout()

    plt.ion()
    plt.show()

    posicao_anterior = None

    for linha, coluna in caminho:
        if posicao_anterior is not None:
            linha_anterior, coluna_anterior = posicao_anterior

            if matriz_visual[linha_anterior][coluna_anterior] == 3:
                matriz_visual[linha_anterior][coluna_anterior] = 0

        if matriz_visual[linha][coluna] == 2:
            matriz_visual[linha][coluna] = 0

        matriz_visual[linha][coluna] = 3

        robo.set_data([coluna], [linha])
        imagem.set_data(matriz_visual)

        posicao_anterior = (linha, coluna)

        plt.pause(intervalo)

    plt.ioff()
    plt.show()