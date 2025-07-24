import networkx
import simpy
import random
import copy
import scipy

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

def gerador_de_pacotes(env: simpy.Environment, no: int, G: networkx.Graph, id_estacao_base: int):
    """Um processo SimPy para um sensor gerar pacotes."""
    while True:
        # Espera um tempo aleatório antes de gerar um novo pacote
        yield env.timeout(random.expovariate(1.0 / 10))
        metricas['pacotes_gerados'] += 1
        pacote = Pacote(
            id_pacote=f'{no}-{metricas["pacotes_gerados"]}',
            origem=no,
            destino=id_estacao_base,
            tempo_de_criacao=env.now
        )
        env.process(roteador(env, no, pacote, G))

def roteador(env: simpy.Environment, no: int, pacote: Pacote, G: networkx.Graph):
    """Um processo SimPy que implementa a lógica de roteamento por inundação."""
    # Se este nó já encaminhou este pacote, descarte-o.
    if pacote.id in pacotes_encaminhados_por_no.get(no, set()):
        return

    # Marca o pacote como encaminhado por este nó.
    pacotes_encaminhados_por_no.setdefault(no, set()).add(pacote.id)

    # Se o pacote chegou à estação base, registra as métricas.
    if no == pacote.destino:
        metricas['pacotes_entregues'] += 1
        metricas['latencias'].append(env.now - pacote.tempo_de_criacao)
        metricas['contagens_de_saltos'].append(pacote.contagem_de_saltos)
        return

    # Incrementa a contagem de encaminhamento para este nó.
    metricas['contagens_de_encaminhamento'][no] = metricas['contagens_de_encaminhamento'].get(no, 0) + 1

    # Inunda o pacote para todos os vizinhos.
    for vizinho in G.neighbors(no):
        # Simula a latência de transmissão.
        yield env.timeout(1)
        
        # Cria uma cópia do pacote para cada transmissão para garantir que a contagem de saltos esteja correta para cada caminho.
        novo_pacote = copy.copy(pacote)
        novo_pacote.contagem_de_saltos += 1
        env.process(roteador(env, vizinho, novo_pacote, G))

def executar_simulacao(G: networkx.Graph, tempo_simulacao: int):
    """
    Configura e executa o ambiente SimPy.

    Args:
        G (networkx.Graph): O grafo da rede.
        tempo_simulacao (int): O tempo total de simulação.

    Returns:
        dict: Um dicionário contendo as métricas da simulação.
    """
    global metricas, pacotes_encaminhados_por_no
    # Reseta o estado para a nova execução da simulação
    metricas = {
        'pacotes_gerados': 0,
        'pacotes_entregues': 0,
        'latencias': [],
        'contagens_de_saltos': [],
        'contagens_de_encaminhamento': {},
        'centralidade_de_grau': {},
        'centralidade_de_intermediacao': {},
        'centralidade_de_proximidade': {},
        'centralidade_de_autovetor': {},
        'centralidade_de_clique': {},
        'centralidade_de_katz': {},
        'centralidade_de_pagerank': {},
        'diametro_rede': 0,
        'is_connected': True
    }
    pacotes_encaminhados_por_no = {}

    # Calcular métricas estruturais do grafo
    metricas['centralidade_de_grau'] = networkx.degree_centrality(G)
    metricas['centralidade_de_intermediacao'] = networkx.betweenness_centrality(G)
    metricas['centralidade_de_proximidade'] = networkx.closeness_centrality(G)
    try:
        metricas['centralidade_de_autovetor'] = networkx.eigenvector_centrality(G, max_iter=1000, tol=1e-05)
    except networkx.PowerIterationFailedConvergence:
        print("Aviso: O cálculo da centralidade de autovetor não convergiu. Os resultados podem ser imprecisos.")
        metricas['centralidade_de_autovetor'] = {node: 0.0 for node in G.nodes()}
    metricas['centralidade_de_clique'] = networkx.clustering(G)
    # metricas['centralidade_de_katz'] = networkx.katz_centrality(G)
    metricas['centralidade_de_pagerank'] = networkx.pagerank(G)

    if networkx.is_connected(G):
        metricas['diametro_rede'] = networkx.diameter(G)
    else: 
        metricas['is_connected'] = False
        componentes_conectados = list(networkx.connected_components(G))
        if componentes_conectados:
            componente_maior = max(componentes_conectados, key=len)
            subgrafo = G.subgraph(componente_maior)
            metricas['diametro_rede'] = networkx.diameter(subgrafo)


    env = simpy.Environment()
    
    # Encontra o ID da estação base
    id_estacao_base = None
    for n, d in G.nodes(data=True):
        if d.get('type') == 'base_station':
            id_estacao_base = n
            break
    
    if id_estacao_base is None:
        raise ValueError("Estação base não encontrada no grafo da rede.")

    # Inicia um gerador de pacotes para cada nó sensor.
    for id_no, dados in G.nodes(data=True):
        if dados.get('type') == 'sensor':
            env.process(gerador_de_pacotes(env, id_no, G, id_estacao_base))

    env.run(until=tempo_simulacao)

    return metricas