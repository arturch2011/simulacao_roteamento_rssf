
import networkx as nx
import random
import math

def criar_grafo_rssf(num_nos=100, tam_area=100, raio_comunicacao=15, pos_estacao_base=(50, 50)):
    """
    Cria um grafo de Rede de Sensores Sem Fio.

    Args:
        num_nos (int): O número de nós sensores.
        tam_area (int): O tamanho da área quadrada.
        raio_comunicacao (int): O raio de comunicação dos nós.
        pos_estacao_base (tuple): A posição da estação base.

    Returns:
        networkx.Graph: O grafo da RSSF.
    """
    G = nx.Graph()
    
    # Adiciona a estação base
    G.add_node(0, id=0, pos=pos_estacao_base, type='base_station', raio_comunicacao=raio_comunicacao)

    # Adiciona os nós sensores
    for i in range(1, num_nos + 1):
        pos = (random.uniform(0, tam_area), random.uniform(0, tam_area))
        G.add_node(i, id=i, pos=pos, type='sensor', raio_comunicacao=raio_comunicacao)

    # Adiciona as arestas com base no raio de comunicação
    for i in G.nodes():
        for j in G.nodes():
            if i != j:
                dist = math.sqrt((G.nodes[i]['pos'][0] - G.nodes[j]['pos'][0])**2 + 
                                 (G.nodes[i]['pos'][1] - G.nodes[j]['pos'][1])**2)
                if dist <= raio_comunicacao:
                    G.add_edge(i, j)

    return G
