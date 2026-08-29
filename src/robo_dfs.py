# Direções possíveis do robô: nome -> (delta_linha, delta_coluna)
# Usamos o MESMO delta tanto para a posição real (dentro do ambiente)
# quanto para a posição relativa do robô (dentro do mapa mental dele).
# Assim as duas coordenadas andam sempre em sincronia, mas o robô nunca
# precisa saber o valor real de sua posição para tomar decisões.

DIRECOES = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}


def sentir(matriz, linhas, colunas, linha_real, coluna_real):
    """
    Sensor do robô: dado APENAS a posição real atual (usada só para saber
    o que existe fisicamente ao redor, nunca exposta à lógica de decisão),
    devolve o que existe nas 4 direções adjacentes.

    "matriz" aqui é a CÓPIA DE TRABALHO (o "mundo físico" que o robô de
    fato percorre e limpa) — nunca a matriz original do ambiente. Isso
    mantém a matriz original intacta, para o visualizador poder mostrar
    onde a sujeira estava e simular a limpeza célula a célula durante a
    animação.

    Fora dos limites da matriz é tratado como obstáculo (parede/limite
    físico do ambiente) — o robô não sabe o tamanho da matriz, só descobre
    "bater na parede" quando tenta sentir/andar para lá.
    """
    percepcoes = {}
    for nome, (dl, dc) in DIRECOES.items():
        nl, nc = linha_real + dl, coluna_real + dc
        if nl < 0 or nl >= linhas or nc < 0 or nc >= colunas:
            percepcoes[nome] = "obstaculo"
        else:
            valor = matriz[nl][nc]
            if valor == 1:
                percepcoes[nome] = "obstaculo"
            elif valor == 2:
                percepcoes[nome] = "sujeira"
            else:
                percepcoes[nome] = "livre"
    return percepcoes


def robo_limpeza_dfs(ambiente, linha_inicial, coluna_inicial):
    """
    Agente de limpeza baseado em Busca em Profundidade "online":
    o robô não conhece o ambiente nem sua posição absoluta. Ele:

      1. Sente as 4 células adjacentes à posição real atual;
      2. Atualiza seu MAPA MENTAL (indexado por coordenadas relativas,
         começando em (0,0) no ponto de partida);
      3. Limpa a célula atual se estiver suja;
      4. Escolhe uma direção ainda não tentada, nesse nó, que leve a uma
         célula conhecida como livre/suja e ainda não visitada;
      5. Se não houver mais direções, RECUA fisicamente um passo (backtrack),
         exatamente como uma pilha de chamadas de DFS recursivo faria -
         só que aqui de forma iterativa, um movimento por vez.

    Importante: o robô nunca limpa a `ambiente.matriz` original. Ele opera
    sobre uma CÓPIA DE TRABALHO própria (o "mundo físico" que ele percorre
    e limpa de fato). A `ambiente.matriz` original fica intacta, com a
    sujeira nas posições originais, justamente para o visualizador poder
    desenhar o estado inicial correto e simular a limpeza acontecendo aos
    poucos, célula por célula, conforme o robô avança no caminho.

    Retorna:
        caminho_real: lista de posições reais (linha, coluna), na ORDEM
                       exata em que o robô fisicamente passou por elas
                       (inclusive recuos) — pronta para animar sem
                       nenhum pós-processamento.
        sujeiras_limpas: quantidade de sujeiras efetivamente limpas.
        mapa_mental: o mapa que o robô construiu sozinho, para depuração.
    """
    linhas, colunas = ambiente.linhas, ambiente.colunas

    # cópia de trabalho: é NELA que o robô efetivamente "limpa" a sujeira.
    # a ambiente.matriz original permanece intacta para a visualização.
    matriz_trabalho = [linha[:] for linha in ambiente.matriz]

    linha_real, coluna_real = linha_inicial, coluna_inicial
    pos_rel = (0, 0)

    mapa_mental = {}       # posicao_relativa -> 'livre'|'obstaculo'|'sujeira'|'limpo'
    visitados = set()      # posicoes relativas onde o robo JA esteve fisicamente
    nao_tentadas = {}       # posicao_relativa -> lista de direcoes ainda por tentar
    pilha_caminho = [pos_rel]     # caminho relativo atual (permite recuar)
    caminho_real = [(linha_real, coluna_real)]
    sujeiras_limpas = 0

    while pilha_caminho:
        atual = pilha_caminho[-1]
        ax, ay = atual

        # 1) sentir o que existe ao redor da posição real correspondente
        percepcoes = sentir(matriz_trabalho, linhas, colunas, linha_real, coluna_real)

        # 2) atualizar o mapa mental com o que foi percebido agora
        for nome, (dl, dc) in DIRECOES.items():
            vizinho_rel = (ax + dl, ay + dc)
            if vizinho_rel not in mapa_mental:
                mapa_mental[vizinho_rel] = percepcoes[nome]

        # 3) primeira vez nesta célula? limpa se estiver suja (na cópia de
        #    trabalho) e calcula quais direções ainda podem ser exploradas
        if atual not in visitados:
            visitados.add(atual)

            if matriz_trabalho[linha_real][coluna_real] == 2:
                matriz_trabalho[linha_real][coluna_real] = 0
                mapa_mental[atual] = "limpo"
                sujeiras_limpas += 1
            elif mapa_mental.get(atual) != "limpo":
                mapa_mental[atual] = "livre"

            candidatas = []
            for nome, (dl, dc) in DIRECOES.items():
                vizinho_rel = (ax + dl, ay + dc)
                estado_vizinho = mapa_mental.get(vizinho_rel)
                if estado_vizinho != "obstaculo" and vizinho_rel not in visitados:
                    candidatas.append(nome)
            nao_tentadas[atual] = candidatas

        # 4) tenta uma direção nova a partir daqui
        if nao_tentadas[atual]:
            direcao = nao_tentadas[atual].pop(0)
            dl, dc = DIRECOES[direcao]

            linha_real += dl
            coluna_real += dc
            pos_rel = (ax + dl, ay + dc)

            pilha_caminho.append(pos_rel)
            caminho_real.append((linha_real, coluna_real))

        # 5) sem mais direções: recua um passo fisicamente (backtrack do DFS)
        else:
            pilha_caminho.pop()
            if pilha_caminho:
                anterior = pilha_caminho[-1]
                dl = anterior[0] - ax
                dc = anterior[1] - ay
                linha_real += dl
                coluna_real += dc
                caminho_real.append((linha_real, coluna_real))

    return caminho_real, sujeiras_limpas, mapa_mental