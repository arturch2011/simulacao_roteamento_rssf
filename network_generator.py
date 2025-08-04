import networkx as nx
import random
import math

def _adicionar_posicoes_aleatorias(G, tam_area=100):
    """Adiciona posições 2D aleatórias a todos os nós de um grafo."""
    for no in G.nodes():
        G.nodes[no]['pos'] = (random.uniform(0, tam_area), random.uniform(0, tam_area))
    return G

def _designar_estacoes_base(G, num_estacoes_base=1):
    """Converte um número de nós aleatórios em estações base."""
    if num_estacoes_base > 0 and len(G.nodes()) >= num_estacoes_base:
        nos_candidatos = list(G.nodes())
        nos_selecionados = random.sample(nos_candidatos, num_estacoes_base)
        for no in nos_selecionados:
            G.nodes[no]['type'] = 'base_station'
    # Define o tipo padrão para os outros nós
    for no in G.nodes():
        if 'type' not in G.nodes[no]:
            G.nodes[no]['type'] = 'sensor'
    return G

def criar_grafo_rssf(num_nos=100, tam_area=100, raio_comunicacao=15, num_estacoes_base=1):
    """
    Cria um grafo de Rede de Sensores Sem Fio (RSSF) com base na proximidade.
    """
    G = nx.Graph()
    
    # Adiciona as estações base em posições aleatórias
    for i in range(num_estacoes_base):
        pos = (random.uniform(0, tam_area), random.uniform(0, tam_area))
        G.add_node(f'base_{i}', id=f'base_{i}', pos=pos, type='base_station', raio_comunicacao=raio_comunicacao)

    # Adiciona os nós sensores
    for i in range(num_nos):
        pos = (random.uniform(0, tam_area), random.uniform(0, tam_area))
        G.add_node(i, id=i, pos=pos, type='sensor', raio_comunicacao=raio_comunicacao)

    # Adiciona as arestas com base no raio de comunicação
    nos = list(G.nodes())
    for i in range(len(nos)):
        for j in range(i + 1, len(nos)):
            no1 = nos[i]
            no2 = nos[j]
            dist = math.sqrt((G.nodes[no1]['pos'][0] - G.nodes[no2]['pos'][0])**2 + 
                             (G.nodes[no1]['pos'][1] - G.nodes[no2]['pos'][1])**2)
            if dist <= raio_comunicacao:
                G.add_edge(no1, no2)

    return G

def criar_grafo_aleatorio(num_nos, p_conexao=0.1, tam_area=100, num_estacoes_base=1):
    """
    Cria um grafo aleatório (Erdős-Rényi) e designa estações base.
    """
    G = nx.erdos_renyi_graph(n=num_nos, p=p_conexao)
    G = _adicionar_posicoes_aleatorias(G, tam_area)
    G = _designar_estacoes_base(G, num_estacoes_base)
    return G

def criar_grafo_barabasi_albert(num_nos, m_conexoes=2, tam_area=100, num_estacoes_base=1):
    """
    Cria um grafo Barabási-Albert e designa estações base.
    """
    if num_nos <= m_conexoes:
        m_conexoes = num_nos - 1 if num_nos > 1 else 1
    G = nx.barabasi_albert_graph(n=num_nos, m=m_conexoes)
    G = _adicionar_posicoes_aleatorias(G, tam_area)
    G = _designar_estacoes_base(G, num_estacoes_base)
    return G

def criar_grafo_watts_strogatz(num_nos, k_vizinhos=4, p_reconectar=0.1, tam_area=100, num_estacoes_base=1):
    """
    Cria um grafo Watts-Strogatz e designa estações base.
    """
    if num_nos <= k_vizinhos:
        k_vizinhos = num_nos - 1 if num_nos > 1 else 1
    G = nx.watts_strogatz_graph(n=num_nos, k=k_vizinhos, p=p_reconectar)
    G = _adicionar_posicoes_aleatorias(G, tam_area)
    G = _designar_estacoes_base(G, num_estacoes_base)
    return G