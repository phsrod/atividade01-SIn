DIRECOES = {"cima": (-1, 0), "baixo": (1, 0), "esquerda": (0, -1), "direita": (0, 1),}


class SensorAmbiente:
    """
    Única porta de entrada entre o robô e o mundo físico.

    O construtor recebe o ambiente e guarda uma cópia de trabalho da
    matriz em um atributo "privado". A partir
    daí, NINGUÉM fora desta classe, nem a função robo_limpeza_dfs, tem
    qualquer referência a essa matriz. As únicas duas operações expostas
    são:

      - sentir(linha, coluna): devolve o que existe nas 4 direções
        adjacentes a uma posição real.
      - limpar_se_sujo(linha, coluna): limpa a posição real atual, se
        estiver suja, e informa se limpou.

    Não existe (e propositalmente não pode existir) nenhum método que
    devolva a matriz inteira, o tamanho do mundo, ou o valor de uma célula
    arbitrária qualquer, só é possível consultar o que está ao redor de
    uma posição por vez, uma consulta de cada vez, exatamente como um
    sensor físico funcionaria.
    """

    def __init__(self, ambiente):
        self._matriz = [linha[:] for linha in ambiente.matriz]

    def sentir(self, linha, coluna):
        percepcoes = {}
        for nome, (dl, dc) in DIRECOES.items():
            nl, nc = linha + dl, coluna + dc
            valor = self._matriz[nl][nc]
            if valor == 1:
                percepcoes[nome] = "obstaculo"
            elif valor == 2:
                percepcoes[nome] = "sujeira"
            else:
                percepcoes[nome] = "livre"
        return percepcoes

    def limpar_se_sujo(self, linha, coluna):
        if self._matriz[linha][coluna] == 2:
            self._matriz[linha][coluna] = 0
            return True
        return False


def robo_limpeza_dfs(sensor, linha_inicial, coluna_inicial):
    """
    Agente de limpeza baseado em Busca em Profundidade "online":
    o robô não conhece o ambiente nem sua posição absoluta. Ele:

      1. Sente as 4 células adjacentes à posição real atual (via
         `sensor.sentir`, nunca acessando matriz nenhuma diretamente);
      2. Atualiza seu MAPA MENTAL (indexado por coordenadas relativas,
         começando em (0,0) no ponto de partida);
      3. Pede ao sensor para limpar a célula atual, se estiver suja;
      4. Escolhe uma direção ainda não tentada, nesse nó, que leve a uma
         célula conhecida como livre/suja e ainda não visitada;
      5. Se não houver mais direções, RECUA fisicamente um passo (backtrack),
         exatamente como uma pilha de chamadas de DFS recursivo faria -
         só que aqui de forma iterativa, um movimento por vez.

    Repare no parâmetro desta função: é "sensor" (um SensorAmbiente), não
    "ambiente" e não "matriz". Isso é intencional — esta função JAMAIS tem
    em mãos uma referência à matriz completa do mundo. Ela só pode
    perguntar ao sensor, uma posição de cada vez, o que existe ao redor.
    Não há como, nem por engano, ler uma célula arbitrária longe da
    posição atual, porque essa possibilidade simplesmente não existe na
    assinatura de nenhum método disponível aqui.

    "linha_inicial"/"coluna_inicial" são a posição real onde o robô nasceu
    (um fato físico inevitável, todo corpo físico ocupa algum lugar),
    usada apenas para inicializar onde o sensor deve consultar a cada
    passo. A lógica de decisão em si (a escolha de direções) nunca usa
    esses valores, só usa o mapa mental e a posição relativa. 

    Retorna:
        caminho_real: lista de posições reais (linha, coluna), na ORDEM
                       exata em que o robô fisicamente passou por elas
                       (inclusive recuos), pronta para animar sem
                       nenhum pós-processamento.
        sujeiras_limpas: quantidade de sujeiras efetivamente limpas.
        mapa_mental: o mapa que o robô construiu sozinho, para depuração.
    """
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

        # 1) sentir o que existe ao redor da posição atual — só através do sensor, nunca lendo uma matriz diretamente
        percepcoes = sensor.sentir(linha_p, coluna_p)

        # 2) atualizar o mapa mental com o que foi percebido agora
        for nome, (dl, dc) in DIRECOES.items():
            vizinho_rel = (ax + dl, ay + dc)
            if vizinho_rel not in mapa_mental:
                mapa_mental[vizinho_rel] = percepcoes[nome]

        # 3) primeira vez nesta célula? pede ao sensor para limpar se estiver suja, e calcula quais direções ainda podem ser exploradas a partir daqui
        if atual not in visitados:
            visitados.add(atual)

            if sensor.limpar_se_sujo(linha_p, coluna_p):
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