
import networkx
import simpy
import random
import copy

# Estado global para a simulação
metricas = {}
pacotes_encaminhados_por_no = {}

class Pacote:
    def __init__(self, id_pacote, origem, destino, tempo_de_criacao):
        self.id = id_pacote
        self.origem = origem
        self.destino = destino
        self.tempo_de_criacao = tempo_de_criacao
        self.contagem_de_saltos = 0

def gerador_de_pacotes(env: simpy.Environment, no: int, G: networkx.Graph, estacoes_base: list):
    """Um processo SimPy para um sensor gerar pacotes para uma estação base aleatória."""
    while True:
        yield env.timeout(random.expovariate(1.0 / 10)) # Intervalo médio de 10s
        metricas['pacotes_gerados'] += 1
        destino_aleatorio = random.choice(estacoes_base)
        pacote = Pacote(
            id_pacote=f'{no}-{metricas["pacotes_gerados"]}',
            origem=no,
            destino=destino_aleatorio,
            tempo_de_criacao=env.now
        )
        env.process(roteador(env, no, pacote, G))

def roteador(env: simpy.Environment, no: int, pacote: Pacote, G: networkx.Graph):
    """Um processo SimPy que implementa a lógica de roteamento por inundação."""
    if pacote.id in pacotes_encaminhados_por_no.get(no, set()):
        return

    pacotes_encaminhados_por_no.setdefault(no, set()).add(pacote.id)

    if no == pacote.destino:
        metricas['pacotes_entregues'] += 1
        metricas['latencias'].append(env.now - pacote.tempo_de_criacao)
        metricas['contagens_de_saltos'].append(pacote.contagem_de_saltos)
        return

    metricas['contagens_de_encaminhamento'][no] = metricas['contagens_de_encaminhamento'].get(no, 0) + 1

    for vizinho in G.neighbors(no):
        yield env.timeout(1) # Latência de transmissão
        novo_pacote = copy.copy(pacote)
        novo_pacote.contagem_de_saltos += 1
        env.process(roteador(env, vizinho, novo_pacote, G))

def executar_simulacao(G: networkx.Graph, tempo_simulacao: int):
    """Configura e executa o ambiente SimPy."""
    global metricas, pacotes_encaminhados_por_no
    metricas = {
        'pacotes_gerados': 0, 'pacotes_entregues': 0, 'latencias': [],
        'contagens_de_saltos': [], 'contagens_de_encaminhamento': {},
        'centralidade_de_grau': {}, 'centralidade_de_intermediacao': {},
        'centralidade_de_proximidade': {}, 'centralidade_de_autovetor': {},
        'centralidade_de_clique': {}, 'centralidade_de_pagerank': {},
        'diametro_rede': 0, 'is_connected': True
    }
    pacotes_encaminhados_por_no = {}

    # Calcular métricas estruturais do grafo (sempre)
    metricas['centralidade_de_grau'] = networkx.degree_centrality(G)
    metricas['centralidade_de_intermediacao'] = networkx.betweenness_centrality(G)
    metricas['centralidade_de_proximidade'] = networkx.closeness_centrality(G)
    try:
        metricas['centralidade_de_autovetor'] = networkx.eigenvector_centrality(G, max_iter=1000, tol=1e-05)
    except (networkx.PowerIterationFailedConvergence, networkx.NetworkXError):
        metricas['centralidade_de_autovetor'] = {node: 0.0 for node in G.nodes()}
    metricas['centralidade_de_clique'] = networkx.clustering(G)
    metricas['centralidade_de_pagerank'] = networkx.pagerank(G)

    if networkx.is_connected(G):
        metricas['diametro_rede'] = networkx.diameter(G)
    else:
        metricas['is_connected'] = False
        componentes = list(networkx.connected_components(G))
        if componentes:
            maior_componente = G.subgraph(max(componentes, key=len))
            metricas['diametro_rede'] = networkx.diameter(maior_componente)

    # Encontra todas as estações base
    estacoes_base = [n for n, d in G.nodes(data=True) if d.get('type') == 'base_station']

    # Executa a simulação de pacotes apenas se houver estações base
    if estacoes_base and tempo_simulacao > 0:
        env = simpy.Environment()
        for id_no, dados in G.nodes(data=True):
            if dados.get('type') != 'base_station':
                env.process(gerador_de_pacotes(env, id_no, G, estacoes_base))
        env.run(until=tempo_simulacao)

    return metricas
