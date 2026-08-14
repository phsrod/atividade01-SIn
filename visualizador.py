import matplotlib.pyplot as plt


def plotar_ambiente(ambiente):

    largura = max(6, ambiente.colunas * 0.45)
    altura = max(6, ambiente.linhas * 0.45)

    fig, ax = plt.subplots(figsize=(largura, altura))

    
    matriz_visual = [[0 for _ in range(ambiente.colunas)] for _ in range(ambiente.linhas)]

    ax.imshow(matriz_visual, cmap="Greys", vmin=0, vmax=1, origin="upper")

    maior_dimensao = max(ambiente.linhas, ambiente.colunas)

    tamanho_elemento = max(4, min(20, 300 / maior_dimensao))
 
    # Percorre todas as posições da matriz.
    for linha in range(ambiente.linhas):
        for coluna in range(ambiente.colunas):

            valor = ambiente.matriz[linha][coluna]

            if valor == 1:
                # Obstáculo
                ax.text(coluna, linha, "■", ha="center", va="center", fontsize=tamanho_elemento, color="black")

            elif valor == 2:
                # Sujeira
                ax.text(coluna, linha,"●", ha="center", va="center", fontsize=tamanho_elemento, color="blue")

            elif valor == 3:
                # Robô
                ax.text(coluna, linha, "R", ha="center", va="center", fontsize=tamanho_elemento, fontweight="bold", color="orange")

    ax.set_xticks(range(ambiente.colunas))

    ax.set_yticks(range(ambiente.linhas))

    ax.set_xticks([i - 0.5 for i in range(ambiente.colunas + 1)], minor=True)

    ax.set_yticks([i - 0.5 for i in range(ambiente.linhas + 1)], minor=True)

    ax.grid(which="minor", color="black", linewidth=0.8)

    ax.set_xticklabels([])

    ax.set_yticklabels([])


    ax.tick_params(which="both", length=0)

    ax.set_aspect("equal")

    plt.tight_layout()

    plt.show()