import networkx as nx
import random
import math

def _adicionar_posicoes_aleatorias(G, tam_area=100):
    """Adiciona posições 2D aleatórias a todos os nós de um grafo."""
    for no in G.nodes():
        G.nodes[no]['pos'] = (random.uniform(0, tam_area), random.uniform(0, tam_area))
        G.nodes[no]['type'] = 'sensor' # Define um tipo padrão
    return G

def criar_grafo_rssf(num_nos=100, tam_area=100, raio_comunicacao=15, num_estacoes_base=1):
    """
    Cria um grafo de Rede de Sensores Sem Fio (RSSF) com base na proximidade.

    Args:
        num_nos (int): O número de nós sensores.
        tam_area (int): O tamanho da área quadrada onde os nós são implantados.
        raio_comunicacao (int): O raio de comunicação dos nós.
        num_estacoes_base (int): O número de estações base a serem criadas.

    Returns:
        networkx.Graph: O grafo da RSSF.
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

def criar_grafo_aleatorio(num_nos, p_conexao=0.1, tam_area=100):
    """
    Cria um grafo aleatório (modelo Erdős-Rényi).

    Args:
        num_nos (int): O número de nós.
        p_conexao (float): A probabilidade de uma aresta ser criada entre dois nós.
        tam_area (int): O tamanho da área para posicionamento visual.

    Returns:
        networkx.Graph: O grafo aleatório.
    """
    G = nx.erdos_renyi_graph(n=num_nos, p=p_conexao)
    G = _adicionar_posicoes_aleatorias(G, tam_area)
    return G

def criar_grafo_barabasi_albert(num_nos, m_conexoes=2, tam_area=100):
    """
    Cria um grafo com o modelo Barabási-Albert (preferential attachment).

    Args:
        num_nos (int): O número de nós.
        m_conexoes (int): O número de arestas para anexar de um novo nó a nós existentes.
        tam_area (int): O tamanho da área para posicionamento visual.

    Returns:
        networkx.Graph: O grafo Barabási-Albert.
    """
    if num_nos <= m_conexoes:
        m_conexoes = num_nos -1 if num_nos > 1 else 1
    G = nx.barabasi_albert_graph(n=num_nos, m=m_conexoes)
    G = _adicionar_posicoes_aleatorias(G, tam_area)
    return G

def criar_grafo_watts_strogatz(num_nos, k_vizinhos=4, p_reconectar=0.1, tam_area=100):
    """
    Cria um grafo "small-world" (modelo Watts-Strogatz).

    Args:
        num_nos (int): O número de nós.
        k_vizinhos (int): O número de vizinhos mais próximos para conectar.
        p_reconectar (float): A probabilidade de reconectar uma aresta.
        tam_area (int): O tamanho da área para posicionamento visual.

    Returns:
        networkx.Graph: O grafo Watts-Strogatz.
    """
    if num_nos <= k_vizinhos:
        k_vizinhos = num_nos -1 if num_nos > 1 else 1
    G = nx.watts_strogatz_graph(n=num_nos, k=k_vizinhos, p=p_reconectar)
    G = _adicionar_posicoes_aleatorias(G, tam_area)
    return G