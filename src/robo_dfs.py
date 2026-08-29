# # Direções possíveis do robô: nome -> (delta_linha, delta_coluna)
# # Usamos o MESMO delta tanto para a posição real (dentro do ambiente)
# # quanto para a posição relativa do robô (dentro do mapa mental dele).
# # Assim as duas coordenadas andam sempre em sincronia, mas o robô nunca
# # precisa saber o valor real de sua posição para tomar decisões.

DIRECOES = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}


def sentir(matriz_com_borda, linha_p, coluna_p):
    """
    Sensor do robô: recebe a posição atual DENTRO DA MATRIZ COM BORDA
    (ver robo_limpeza_dfs) e devolve o que existe nas 4 direções.

    Importante: essa função NÃO faz nenhuma comparação com o tamanho da
    matriz. A matriz recebida já vem cercada por uma moldura de obstáculos
    de verdade (valor 1), então "sair do ambiente real" e "esbarrar num
    obstáculo interno" são, aqui, exatamente a mesma operação: olhar
    matriz_com_borda[nl][nc] e achar o valor 1. O sensor nunca sabe (nem
    precisa saber) se aquele obstáculo é uma parede do mundo ou um
    obstáculo sorteado no meio do caminho — para ele são a mesma coisa.
    """
    percepcoes = {}
    for nome, (dl, dc) in DIRECOES.items():
        nl, nc = linha_p + dl, coluna_p + dc
        valor = matriz_com_borda[nl][nc]
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

    Como o ambiente termina sem paredes explícitas: em vez de o sensor
    comparar índices com "linhas"/"colunas" (o que dava a impressão de
    estar consultando o tamanho do mapa, mesmo sem vazar essa informação
    pra decisão do robô), aqui construímos uma CÓPIA DE TRABALHO cercada
    por uma moldura de obstáculos de verdade (valor 1) ao redor de toda a
    borda. Isso é feito UMA ÚNICA VEZ, na "criação do mundo", antes do
    robô dar o primeiro passo — o mesmo tipo de operação que ambiente.py
    já faz ao sortear os obstáculos internos. A partir daí, o sensor nunca
    mais faz nenhuma conta com o tamanho da matriz: sair do ambiente real
    e bater num obstáculo interno viram, literalmente, a mesma leitura de
    valor 1 numa célula.

    Retorna:
        caminho_real: lista de posições reais (linha, coluna), na ORDEM
                       exata em que o robô fisicamente passou por elas
                       (inclusive recuos) — pronta para animar sem
                       nenhum pós-processamento.
        sujeiras_limpas: quantidade de sujeiras efetivamente limpas.
        mapa_mental: o mapa que o robô construiu sozinho, para depuração.
    """
    colunas = ambiente.colunas
    matriz_trabalho = [linha[:] for linha in ambiente.matriz]

    # moldura de obstáculos ao redor da cópia de trabalho
    largura_com_borda = colunas + 2
    matriz_com_borda = [[1] * largura_com_borda]
    for linha in matriz_trabalho:
        matriz_com_borda.append([1] + linha + [1])
    matriz_com_borda.append([1] * largura_com_borda)

    # toda posição real (linha_real, coluna_real) corresponde a
    # (linha_real + 1, coluna_real + 1) dentro da matriz com borda —
    # um deslocamento fixo, não uma consulta ao tamanho do ambiente
    linha_p, coluna_p = linha_inicial + 1, coluna_inicial + 1
    pos_rel = (0, 0)

    mapa_mental = {}       # posicao_relativa -> 'livre'|'obstaculo'|'sujeira'|'limpo'
    visitados = set()      # posicoes relativas onde o robo JA esteve fisicamente
    nao_tentadas = {}       # posicao_relativa -> lista de direcoes ainda por tentar
    pilha_caminho = [pos_rel]     # caminho relativo atual (permite recuar)
    caminho_real = [(linha_inicial, coluna_inicial)]
    sujeiras_limpas = 0

    while pilha_caminho:
        atual = pilha_caminho[-1]
        ax, ay = atual

        # 1) sentir o que existe ao redor da posição atual (na matriz com borda)
        percepcoes = sentir(matriz_com_borda, linha_p, coluna_p)

        # 2) atualizar o mapa mental com o que foi percebido agora
        for nome, (dl, dc) in DIRECOES.items():
            vizinho_rel = (ax + dl, ay + dc)
            if vizinho_rel not in mapa_mental:
                mapa_mental[vizinho_rel] = percepcoes[nome]

        # 3) primeira vez nesta célula? limpa se estiver suja e calcula
        #    quais direções ainda podem ser exploradas a partir daqui
        if atual not in visitados:
            visitados.add(atual)

            if matriz_com_borda[linha_p][coluna_p] == 2:
                matriz_com_borda[linha_p][coluna_p] = 0
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

            linha_p += dl
            coluna_p += dc
            pos_rel = (ax + dl, ay + dc)

            pilha_caminho.append(pos_rel)
            caminho_real.append((linha_p - 1, coluna_p - 1))  # de volta às coordenadas reais (sem borda)

        # 5) sem mais direções: recua um passo fisicamente (backtrack do DFS)
        else:
            pilha_caminho.pop()
            if pilha_caminho:
                anterior = pilha_caminho[-1]
                dl = anterior[0] - ax
                dc = anterior[1] - ay
                linha_p += dl
                coluna_p += dc
                caminho_real.append((linha_p - 1, coluna_p - 1))

    return caminho_real, sujeiras_limpas, mapa_mental