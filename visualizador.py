import matplotlib.pyplot as plt


def criar_matriz_visual(ambiente):
    matriz = []

    for linha in range(ambiente.linhas):
        nova_linha = []

        for coluna in range(ambiente.colunas):
            nova_linha.append(0)

        matriz.append(nova_linha)

    return matriz


def calcular_tamanho_figura(ambiente):
    largura = ambiente.colunas * 0.45
    altura = ambiente.linhas * 0.45

    if largura < 6:
        largura = 6

    if altura < 6:
        altura = 6

    return largura, altura


def calcular_tamanho_elemento(ambiente):
    maior_dimensao = max(ambiente.linhas, ambiente.colunas)

    tamanho = 300 / maior_dimensao

    if tamanho < 4:
        tamanho = 4

    if tamanho > 20:
        tamanho = 20

    return tamanho


def configurar_grade(ax, ambiente):
    ax.set_xticks(range(ambiente.colunas))
    ax.set_yticks(range(ambiente.linhas))

    linhas_grade = []

    for i in range(ambiente.colunas + 1):
        linhas_grade.append(i - 0.5)

    colunas_grade = []

    for i in range(ambiente.linhas + 1):
        colunas_grade.append(i - 0.5)

    ax.set_xticks(linhas_grade, minor=True)
    ax.set_yticks(colunas_grade, minor=True)

    ax.grid(which="minor", color="black",linewidth=0.8)

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.tick_params(which="both", length=0)

    ax.set_aspect("equal")


def plotar_ambiente(ambiente):
    largura, altura = calcular_tamanho_figura(ambiente)

    fig, ax = plt.subplots(figsize=(largura, altura))

    matriz_visual = criar_matriz_visual(ambiente)

    ax.imshow(matriz_visual, cmap="Greys", vmin=0, vmax=1, origin="upper")

    tamanho_elemento = calcular_tamanho_elemento(ambiente)

    for linha in range(ambiente.linhas):
        for coluna in range(ambiente.colunas):
            valor = ambiente.matriz[linha][coluna]

            if valor == 1:
                ax.text(coluna, linha, "■", ha="center", va="center", fontsize=tamanho_elemento, color="black")

            elif valor == 2:
                ax.text(coluna, linha, "●", ha="center", va="center", fontsize=tamanho_elemento, color="blue")

            elif valor == 3:
                ax.text(coluna, linha, "R", ha="center", va="center", fontsize=tamanho_elemento, fontweight="bold", color="red")

    configurar_grade(ax, ambiente)

    plt.tight_layout()
    plt.show()


def andar(posicao, restantes, caminho):
    linha = posicao[0]
    coluna = posicao[1]
    vizinhos = [(linha + 1, coluna), (linha - 1, coluna), (linha, coluna + 1), (linha, coluna - 1)]

    for vizinho in vizinhos:
        if vizinho in restantes:
            restantes.remove(vizinho)
            caminho.append(vizinho)
            andar(vizinho, restantes, caminho)
            caminho.append(posicao)


def gerar_caminho_continuo(visitados):
    restantes = set(visitados)
    primeira_posicao = visitados[0]
    restantes.remove(primeira_posicao)
    caminho = [primeira_posicao]
    andar(primeira_posicao, restantes, caminho)
    return caminho


def animar_limpeza(ambiente, caminho, intervalo=0.05):
    caminho = gerar_caminho_continuo(caminho)

    largura, altura = calcular_tamanho_figura(ambiente)

    fig, ax = plt.subplots(figsize=(largura, altura))

    matriz_visual = criar_matriz_visual(ambiente)

    ax.imshow(matriz_visual, cmap="Greys", vmin=0, vmax=1, origin="upper")

    tamanho_elemento = calcular_tamanho_elemento(ambiente)

    sujeiras = {}

    for linha in range(ambiente.linhas):
        for coluna in range(ambiente.colunas):

            valor = ambiente.matriz[linha][coluna]

            if valor == 1:
                ax.text(coluna, linha, "■", ha="center", va="center", fontsize=tamanho_elemento, color="black")

            elif valor == 2:
                sujeira = ax.text(coluna, linha, "●", ha="center", va="center", fontsize=tamanho_elemento, color="blue")

                sujeiras[(linha, coluna)] = sujeira

    configurar_grade(ax, ambiente)

    linha_robo = ambiente.posicao_robo[0]
    coluna_robo = ambiente.posicao_robo[1]

    robo = ax.text(coluna_robo, linha_robo, "R", ha="center", va="center", fontsize=tamanho_elemento, fontweight="bold", color="red")

    plt.tight_layout()

    plt.ion()
    plt.show()

    for passo in caminho:
        linha = passo[0]
        coluna = passo[1]

        if (linha, coluna) in sujeiras:
            sujeiras[(linha, coluna)].set_text("")

            del sujeiras[(linha, coluna)]

        robo.set_position((coluna, linha))

        plt.pause(intervalo)

    plt.ioff()
    plt.show()