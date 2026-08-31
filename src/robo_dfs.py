from ambiente import DIRECOES


class SensorAmbiente:
    """
    Única porta de entrada entre o robô e o mundo físico.

    O Ambiente guarda a matriz, a posição absoluta e o estado físico do
    robô. Esta classe expõe ao DFS somente as operações permitidas:

      - sentir(): devolve o que existe nas 4 direções adjacentes.
      - mover(direcao): tenta realizar um movimento físico.
      - limpar_se_sujo(): limpa a posição atual, se estiver suja.

    Não há método que devolva a matriz, seu tamanho, coordenadas reais ou
    o valor de uma célula arbitrária. O DFS não recebe coordenadas nem
    referências à matriz.
    """

    def __init__(self, ambiente):
        self._ambiente = ambiente

    def sentir(self):
        return self._ambiente.sentir_arredores()

    def mover(self, direcao):
        return self._ambiente.mover_robo(direcao)

    def limpar_se_sujo(self):
        return self._ambiente.limpar_posicao_robo()


def robo_limpeza_dfs(sensor):
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
    perguntar ao sensor o que existe ao redor. Não há como informar ou
    obter uma posição absoluta, nem ler uma célula arbitrária distante:
    essa possibilidade não existe na assinatura dos métodos disponíveis.

    Retorna:
        sujeiras_limpas: quantidade de sujeiras efetivamente limpas.
        mapa_mental: o mapa que o robô construiu sozinho, para depuração.
    """
    pos_rel = (0, 0)

    mapa_mental = {}       # posicao_relativa -> 'livre'|'obstaculo'|'sujeira'|'limpo'
    visitados = set()      # posicoes relativas onde o robo JA esteve fisicamente
    nao_tentadas = {}       # posicao_relativa -> lista de direcoes ainda por tentar
    pilha_caminho = [pos_rel]     # caminho relativo atual (permite recuar)
    sujeiras_limpas = 0

    while pilha_caminho:
        atual = pilha_caminho[-1]
        ax, ay = atual

        # 1) sentir o que existe ao redor da posição atual — só através do sensor, nunca lendo uma matriz diretamente
        percepcoes = sensor.sentir()

        # 2) atualizar o mapa mental com o que foi percebido agora
        for nome, (dl, dc) in DIRECOES.items():
            vizinho_rel = (ax + dl, ay + dc)
            if vizinho_rel not in mapa_mental:
                mapa_mental[vizinho_rel] = percepcoes[nome]

        # 3) primeira vez nesta célula? pede ao sensor para limpar se estiver suja, e calcula quais direções ainda podem ser exploradas a partir daqui
        if atual not in visitados:
            visitados.add(atual)

            if sensor.limpar_se_sujo():
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

            pos_rel = (ax + dl, ay + dc)
            if not sensor.mover(direcao):
                raise RuntimeError("O sensor informou caminho livre e bloqueou o movimento.")
            pilha_caminho.append(pos_rel)

        # 5) sem mais direções: recua um passo fisicamente (backtrack do DFS)
        else:
            pilha_caminho.pop()
            if pilha_caminho:
                anterior = pilha_caminho[-1]
                dl = anterior[0] - ax
                dc = anterior[1] - ay
                direcao_recuo = next(
                    nome for nome, deslocamento in DIRECOES.items()
                    if deslocamento == (dl, dc)
                )
                if not sensor.mover(direcao_recuo):
                    raise RuntimeError("Não foi possível recuar para uma célula já visitada.")

    return sujeiras_limpas, mapa_mental
