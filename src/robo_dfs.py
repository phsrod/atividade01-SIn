# Direções possíveis do robô: nome -> (delta_linha, delta_coluna)
DIRECOES = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}


def sentir(matriz, linha_p, coluna_p):
    """
    Sensor do robô: recebe a posição atual DENTRO DA MATRIZ REAL (que já
    nasce com uma moldura de obstáculos ao redor — ver ambiente.py) e
    devolve o que existe nas 4 direções.

    Não faz nenhuma comparação com tamanho de mundo nenhum: só lê o valor
    guardado em matriz[nl][nc]. Sair da área útil e esbarrar num obstáculo
    interno são a mesma leitura de valor 1.
    """
    percepcoes = {}
    for nome, (dl, dc) in DIRECOES.items():
        nl, nc = linha_p + dl, coluna_p + dc
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

    Este módulo NUNCA lê ambiente.linhas nem ambiente.colunas. A moldura de
    obstáculos que representa o limite do mundo já vem PRONTA dentro de
    ambiente.matriz (construída em ambiente.py, na "criação do mundo",
    antes de qualquer robô existir) — aqui só copiamos essa matriz para
    uma cópia de trabalho e andamos sobre ela.

    "linha_inicial"/"coluna_inicial" estão em coordenadas da ÁREA ÚTIL
    (sem moldura, ex.: (0,0) é o canto real do ambiente). Como a matriz diz
    respeito à área útil cercada por +1 célula de moldura de cada lado, a
    posição correspondente dentro dela é sempre (linha_inicial + 1,
    coluna_inicial + 1) — um deslocamento fixo de convenção, não uma
    consulta ao tamanho do mundo.

    Retorna:
        caminho_real: lista de posições reais (linha, coluna), na ORDEM
                       exata em que o robô fisicamente passou por elas
                       (inclusive recuos) — pronta para animar sem
                       nenhum pós-processamento.
        sujeiras_limpas: quantidade de sujeiras efetivamente limpas.
        mapa_mental: o mapa que o robô construiu sozinho, para depuração.
    """
    matriz_trabalho = [linha[:] for linha in ambiente.matriz]

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

        # 1) sentir o que existe ao redor da posição atual
        percepcoes = sentir(matriz_trabalho, linha_p, coluna_p)

        # 2) atualizar o mapa mental com o que foi percebido agora
        for nome, (dl, dc) in DIRECOES.items():
            vizinho_rel = (ax + dl, ay + dc)
            if vizinho_rel not in mapa_mental:
                mapa_mental[vizinho_rel] = percepcoes[nome]

        # 3) primeira vez nesta célula? limpa se estiver suja e calcula
        #    quais direções ainda podem ser exploradas a partir daqui
        if atual not in visitados:
            visitados.add(atual)

            if matriz_trabalho[linha_p][coluna_p] == 2:
                matriz_trabalho[linha_p][coluna_p] = 0
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
            caminho_real.append((linha_p - 1, coluna_p - 1))

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