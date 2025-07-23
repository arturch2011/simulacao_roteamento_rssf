
import matplotlib.pyplot as plt
import networkx as nx

def plotar_rede(G):
    """
    Plota a topologia da rede.

    Args:
        G (networkx.Graph): O grafo da rede.
    """
    pos = nx.get_node_attributes(G, 'pos')
    cores_nos = ['red' if G.nodes[n]['type'] == 'base_station' else 'blue' for n in G.nodes()]
    
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=50, node_color=cores_nos, font_size=8)
    plt.title("Topologia da Rede de Sensores Sem Fio")
    plt.show()

def plotar_metricas(metrics):
    """
    Plota as métricas da simulação.

    Args:
        metrics (dict): Um dicionário contendo as métricas da simulação.
    """
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.hist(metrics['latencias'], bins=20)
    plt.title("Distribuição de Latência")
    plt.xlabel("Latência")
    plt.ylabel("Frequência")

    plt.subplot(1, 3, 2)
    plt.hist(metrics['contagens_de_saltos'], bins=10)
    plt.title("Distribuição de Saltos")
    plt.xlabel("Número de Saltos")
    plt.ylabel("Frequência")

    plt.subplot(1, 3, 3)
    gargalos = sorted(metrics['contagens_de_encaminhamento'].items(), key=lambda x: x[1], reverse=True)[:10]
    nos, contagens = zip(*gargalos)
    plt.bar(range(len(nos)), contagens, tick_label=nos)
    plt.title("Top 10 Nós de Gargalo")
    plt.xlabel("ID do Nó")
    plt.ylabel("Contagem de Encaminhamentos")

    plt.tight_layout()
    plt.show()
