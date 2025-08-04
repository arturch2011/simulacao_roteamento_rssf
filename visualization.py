import matplotlib.pyplot as plt
import networkx as nx

def plotar_rede(G):
    """
    Cria e retorna uma figura Matplotlib da topologia da rede.

    Args:
        G (networkx.Graph): O grafo da rede.

    Returns:
        matplotlib.figure.Figure: A figura contendo o gráfico da rede.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    pos = nx.get_node_attributes(G, 'pos')
    
    # Define a cor com base no tipo de nó, com um padrão para tipos não especificados
    cores_nos = []
    for n in G.nodes():
        node_type = G.nodes[n].get('type', 'sensor') # Padrão para 'sensor' se o tipo não existir
        if node_type == 'base_station':
            cores_nos.append('red')
        else:
            cores_nos.append('blue')

    nx.draw(G, pos, ax=ax, with_labels=True, node_size=50, node_color=cores_nos, font_size=8)
    ax.set_title("Topologia da Rede")
    return fig

def plotar_metricas(metrics):
    """
    Cria e retorna uma figura Matplotlib com as métricas da simulação.

    Args:
        metrics (dict): Um dicionário contendo as métricas da simulação.

    Returns:
        matplotlib.figure.Figure: A figura contendo os gráficos de métricas.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Gráfico de Latência
    if metrics.get('latencias'):
        axes[0].hist(metrics['latencias'], bins=20, color='skyblue')
        axes[0].set_title("Distribuição de Latência")
        axes[0].set_xlabel("Latência")
        axes[0].set_ylabel("Frequência")
    else:
        axes[0].text(0.5, 0.5, 'Sem dados de latência', ha='center', va='center')
        axes[0].set_title("Distribuição de Latência")

    # Gráfico de Saltos
    if metrics.get('contagens_de_saltos'):
        axes[1].hist(metrics['contagens_de_saltos'], bins=10, color='lightgreen')
        axes[1].set_title("Distribuição de Saltos")
        axes[1].set_xlabel("Número de Saltos")
        axes[1].set_ylabel("Frequência")
    else:
        axes[1].text(0.5, 0.5, 'Sem dados de saltos', ha='center', va='center')
        axes[1].set_title("Distribuição de Saltos")

    # Gráfico de Nós de Gargalo
    if metrics.get('contagens_de_encaminhamento'):
        gargalos = sorted(metrics['contagens_de_encaminhamento'].items(), key=lambda x: x[1], reverse=True)[:10]
        if gargalos:
            nos, contagens = zip(*gargalos)
            # Converte todos os rótulos para string para evitar erros de tipo
            str_nos = [str(n) for n in nos]
            axes[2].bar(str_nos, contagens, color='salmon')
            axes[2].set_title("Top 10 Nós de Gargalo")
            axes[2].set_xlabel("ID do Nó")
            axes[2].set_ylabel("Contagem de Encaminhamentos")
            axes[2].tick_params(axis='x', rotation=45)
        else:
            axes[2].text(0.5, 0.5, 'Sem dados de encaminhamento', ha='center', va='center')
            axes[2].set_title("Top 10 Nós de Gargalo")
    else:
        axes[2].text(0.5, 0.5, 'Sem dados de encaminhamento', ha='center', va='center')
        axes[2].set_title("Top 10 Nós de Gargalo")

    plt.tight_layout()
    return fig