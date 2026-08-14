import matplotlib.pyplot as plt


def plotar_ambiente(ambiente):

    fig, ax = plt.subplots()

    
    matriz_visual = [[0 for _ in range(ambiente.colunas)] for _ in range(ambiente.linhas)]

    ax.imshow(matriz_visual, cmap="Greys", vmin=0, vmax=1)

    # Percorre todas as posições da matriz.
    for linha in range(ambiente.linhas):
        for coluna in range(ambiente.colunas):

            valor = ambiente.matriz[linha][coluna]

            if valor == 1:
                # Obstáculo
                ax.text(coluna, linha, "■", ha="center", va="center", fontsize=20, color="black")

            elif valor == 2:
                # Sujeira
                ax.text(coluna, linha,"●", ha="center", va="center", fontsize=18, color="blue")

            elif valor == 3:
                # Robô
                ax.text(coluna, linha, "R", ha="center", va="center", fontsize=18, fontweight="bold", color="gold")

    # Configura a grade da matriz.
    ax.set_xticks(range(ambiente.colunas))
    ax.set_yticks(range(ambiente.linhas))

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.grid(True, linewidth=0.8)

    ax.set_title("Estado inicial do ambiente")

    plt.show()