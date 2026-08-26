import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


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
        "white",  # 0: espaco livre
        "black",  # 1: obstaculo
        "blue",   # 2: sujeira
        "red",    # 3: robo
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
    stack = [(posicao, 0)]

    while stack:
        pos, idx = stack[-1]

        if pos in restantes:
            restantes.discard(pos)
            caminho.append(pos)

        linha, coluna = pos
        vizinhos = [
            (linha + 1, coluna),
            (linha - 1, coluna),
            (linha, coluna + 1),
            (linha, coluna - 1),
        ]

        # procura proximo vizinho nao visitado
        encontrou = False
        while idx < 4:
            if vizinhos[idx] in restantes:
                stack[-1] = (pos, idx + 1)
                stack.append((vizinhos[idx], 0))
                encontrou = True
                break
            idx += 1

        if not encontrou:
            stack.pop()
            if stack:
                caminho.append(stack[-1][0])


def gerar_caminho_continuo(visitados):
    if not visitados:
        return []

    restantes = set(visitados)
    primeira_posicao = visitados[0]
    restantes.remove(primeira_posicao)

    caminho = [primeira_posicao]
    restantes.add(primeira_posicao)
    andar(primeira_posicao, restantes, caminho)

    # remove duplicata da posicao inicial
    if len(caminho) > 1 and caminho[0] == caminho[1]:
        caminho.pop(1)

    return caminho


def animar_limpeza(ambiente, caminho, intervalo=0.05):
    caminho = gerar_caminho_continuo(caminho)

    if not caminho:
        return

    largura, altura = calcular_tamanho_figura(ambiente)
    cores = criar_mapa_cores()

    matriz_visual = np.array(ambiente.matriz, dtype=int)

    linha_robo, coluna_robo = ambiente.posicao_robo
    matriz_visual[linha_robo][coluna_robo] = 0

    total_passos = len(caminho)

    # para grades grandes, multiplos passos por frame
    passos_por_frame = max(1, total_passos // 5000)
    total_frames = (total_passos + passos_por_frame - 1) // passos_por_frame

    # intervalo adaptativo
    fps = min(60, max(1, int(1 / intervalo))) if intervalo > 0 else 60
    intervalo_ms = 1000 / fps

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

    # plt.tight_layout()
    indice_global = [0]
    posicao_anterior = [None]
    ultima_posicao = [linha_robo, coluna_robo]

    def atualizar(frame):
        inicio = indice_global[0]
        fim = min(inicio + passos_por_frame, total_passos)

        for k in range(inicio, fim):
            linha, coluna = caminho[k]

            if posicao_anterior[0] is not None:
                la, ca = posicao_anterior[0]
                if matriz_visual[la][ca] == 3:
                    matriz_visual[la][ca] = 0

            if matriz_visual[linha][coluna] == 2:
                matriz_visual[linha][coluna] = 0

            matriz_visual[linha][coluna] = 3
            posicao_anterior[0] = (linha, coluna)
            ultima_posicao[0] = linha
            ultima_posicao[1] = coluna

        indice_global[0] = fim

        robo.set_data([ultima_posicao[1]], [ultima_posicao[0]])
        imagem.set_data(matriz_visual)

        return robo, imagem

    anim = FuncAnimation(
        fig,
        atualizar,
        frames=total_frames,
        interval=intervalo_ms,
        blit=True,
        repeat=False,
    )

    plt.show()
