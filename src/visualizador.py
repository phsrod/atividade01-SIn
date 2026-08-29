# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
# from matplotlib.animation import FuncAnimation


# def calcular_tamanho_figura(ambiente):
#     maior_dimensao = max(ambiente.linhas, ambiente.colunas)

#     if maior_dimensao <= 20:
#         escala = 0.45
#     else:
#         escala = 10 / maior_dimensao

#     largura = max(4, ambiente.colunas * escala)
#     altura = max(4, ambiente.linhas * escala)

#     return largura, altura


# def configurar_grade(ax, ambiente):
#     if ambiente.linhas > 50 or ambiente.colunas > 50:
#         ax.set_xticks([])
#         ax.set_yticks([])
#         return

#     ax.set_xticks(range(ambiente.colunas))
#     ax.set_yticks(range(ambiente.linhas))

#     ax.set_xticks(
#         [i - 0.5 for i in range(ambiente.colunas + 1)],
#         minor=True
#     )

#     ax.set_yticks(
#         [i - 0.5 for i in range(ambiente.linhas + 1)],
#         minor=True
#     )

#     ax.grid(
#         which="minor",
#         color="black",
#         linewidth=0.8
#     )

#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     ax.tick_params(which="both", length=0)
#     ax.set_aspect("equal")


# def criar_mapa_cores():
#     return ListedColormap([
#         "white",  # 0: espaco livre
#         "black",  # 1: obstaculo
#         "blue",   # 2: sujeira
#         "red",    # 3: robo
#     ])


# def plotar_ambiente(ambiente):
#     largura, altura = calcular_tamanho_figura(ambiente)
#     cores = criar_mapa_cores()

#     fig, ax = plt.subplots(figsize=(largura, altura))

#     ax.imshow(
#         ambiente.matriz,
#         cmap=cores,
#         vmin=0,
#         vmax=3,
#         interpolation="nearest",
#         origin="upper"
#     )

#     configurar_grade(ax, ambiente)

#     plt.tight_layout()
#     plt.show()


# def animar_limpeza(ambiente, caminho, intervalo=0.05):
#     # "caminho" já vem pronto do robô: é a sequência real de posições por
#     # onde ele passou fisicamente, passo a passo, incluindo os recuos do
#     # backtracking do DFS. Não há necessidade de reconstruir nada aqui.
#     if not caminho:
#         return

#     largura, altura = calcular_tamanho_figura(ambiente)
#     cores = criar_mapa_cores()

#     matriz_visual = np.array(ambiente.matriz, dtype=int)

#     linha_robo, coluna_robo = ambiente.posicao_robo
#     matriz_visual[linha_robo][coluna_robo] = 0

#     total_passos = len(caminho)

#     # para grades grandes, multiplos passos por frame
#     passos_por_frame = max(1, total_passos // 5000)
#     total_frames = (total_passos + passos_por_frame - 1) // passos_por_frame

#     # intervalo adaptativo
#     fps = min(60, max(1, int(1 / intervalo))) if intervalo > 0 else 60
#     intervalo_ms = 1000 / fps

#     fig, ax = plt.subplots(figsize=(largura, altura))

#     imagem = ax.imshow(
#         matriz_visual,
#         cmap=cores,
#         vmin=0,
#         vmax=3,
#         interpolation="nearest",
#         origin="upper"
#     )

#     configurar_grade(ax, ambiente)

#     robo, = ax.plot(
#         coluna_robo,
#         linha_robo,
#         marker="o",
#         markersize=6,
#         color="red"
#     )

#     # plt.tight_layout()
#     indice_global = [0]
#     posicao_anterior = [None]
#     ultima_posicao = [linha_robo, coluna_robo]

#     def atualizar(frame):
#         inicio = indice_global[0]
#         fim = min(inicio + passos_por_frame, total_passos)

#         for k in range(inicio, fim):
#             linha, coluna = caminho[k]

#             if posicao_anterior[0] is not None:
#                 la, ca = posicao_anterior[0]
#                 if matriz_visual[la][ca] == 3:
#                     matriz_visual[la][ca] = 0

#             if matriz_visual[linha][coluna] == 2:
#                 matriz_visual[linha][coluna] = 0

#             matriz_visual[linha][coluna] = 3
#             posicao_anterior[0] = (linha, coluna)
#             ultima_posicao[0] = linha
#             ultima_posicao[1] = coluna

#         indice_global[0] = fim

#         robo.set_data([ultima_posicao[1]], [ultima_posicao[0]])
#         imagem.set_data(matriz_visual)

#         return robo, imagem

#     anim = FuncAnimation(
#         fig,
#         atualizar,
#         frames=total_frames,
#         interval=intervalo_ms,
#         blit=True,
#         repeat=False,
#     )

#     plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


def adicionar_borda(matriz, linhas, colunas):
    """
    Cerca a matriz original com uma moldura de obstáculos (valor 1) em
    todos os lados — a MESMA moldura que o robô usa internamente
    (ver robo_dfs.py) para nunca precisar comparar índices com o tamanho
    do ambiente. Aqui ela serve só para EXIBIÇÃO: mostrar visualmente que,
    para o robô, "sair do ambiente" e "bater num obstáculo" são a mesma
    coisa.

    Uma matriz linhas x colunas vira (linhas + 2) x (colunas + 2).
    """
    largura_com_borda = colunas + 2
    matriz_com_borda = [[1] * largura_com_borda]
    for linha in matriz:
        matriz_com_borda.append([1] + list(linha) + [1])
    matriz_com_borda.append([1] * largura_com_borda)
    return matriz_com_borda


def calcular_tamanho_figura(linhas, colunas):
    maior_dimensao = max(linhas, colunas)

    if maior_dimensao <= 20:
        escala = 0.45
    else:
        escala = 10 / maior_dimensao

    largura = max(4, colunas * escala)
    altura = max(4, linhas * escala)

    return largura, altura


def configurar_grade(ax, linhas, colunas):
    if linhas > 50 or colunas > 50:
        ax.set_xticks([])
        ax.set_yticks([])
        return

    ax.set_xticks(range(colunas))
    ax.set_yticks(range(linhas))

    ax.set_xticks(
        [i - 0.5 for i in range(colunas + 1)],
        minor=True
    )

    ax.set_yticks(
        [i - 0.5 for i in range(linhas + 1)],
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
        "black",  # 1: obstaculo (inclui a moldura das bordas)
        "blue",   # 2: sujeira
        "red",    # 3: robo
    ])


def plotar_ambiente(ambiente):
    linhas_exib = ambiente.linhas + 2
    colunas_exib = ambiente.colunas + 2

    matriz_exib = adicionar_borda(ambiente.matriz, ambiente.linhas, ambiente.colunas)

    largura, altura = calcular_tamanho_figura(linhas_exib, colunas_exib)
    cores = criar_mapa_cores()

    fig, ax = plt.subplots(figsize=(largura, altura))

    ax.imshow(
        matriz_exib,
        cmap=cores,
        vmin=0,
        vmax=3,
        interpolation="nearest",
        origin="upper"
    )

    configurar_grade(ax, linhas_exib, colunas_exib)

    plt.tight_layout()
    plt.show()


def animar_limpeza(ambiente, caminho, intervalo=0.05):
    # "caminho" já vem pronto do robô: é a sequência real de posições por
    # onde ele passou fisicamente, passo a passo, incluindo os recuos do
    # backtracking do DFS. Essas posições estão em coordenadas REAIS (sem
    # a moldura) — por isso somamos +1 abaixo, para alinhar com a matriz
    # de exibição, que tem a moldura de obstáculos ao redor.
    if not caminho:
        return

    linhas_exib = ambiente.linhas + 2
    colunas_exib = ambiente.colunas + 2

    largura, altura = calcular_tamanho_figura(linhas_exib, colunas_exib)
    cores = criar_mapa_cores()

    matriz_visual = np.array(
        adicionar_borda(ambiente.matriz, ambiente.linhas, ambiente.colunas),
        dtype=int
    )

    linha_robo, coluna_robo = ambiente.posicao_robo
    linha_robo_exib, coluna_robo_exib = linha_robo + 1, coluna_robo + 1
    matriz_visual[linha_robo_exib][coluna_robo_exib] = 0

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

    configurar_grade(ax, linhas_exib, colunas_exib)

    robo, = ax.plot(
        coluna_robo_exib,
        linha_robo_exib,
        marker="o",
        markersize=6,
        color="red"
    )

    indice_global = [0]
    posicao_anterior = [None]
    ultima_posicao = [linha_robo_exib, coluna_robo_exib]

    def atualizar(frame):
        inicio = indice_global[0]
        fim = min(inicio + passos_por_frame, total_passos)

        for k in range(inicio, fim):
            linha, coluna = caminho[k]
            linha_exib, coluna_exib = linha + 1, coluna + 1

            if posicao_anterior[0] is not None:
                la, ca = posicao_anterior[0]
                if matriz_visual[la][ca] == 3:
                    matriz_visual[la][ca] = 0

            if matriz_visual[linha_exib][coluna_exib] == 2:
                matriz_visual[linha_exib][coluna_exib] = 0

            matriz_visual[linha_exib][coluna_exib] = 3
            posicao_anterior[0] = (linha_exib, coluna_exib)
            ultima_posicao[0] = linha_exib
            ultima_posicao[1] = coluna_exib

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