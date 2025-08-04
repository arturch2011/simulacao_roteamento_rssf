import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

def plotar_rede(G):
    """
    Cria e retorna uma figura Plotly interativa da topologia da rede.
    """
    pos = nx.get_node_attributes(G, 'pos')
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_info = f"ID: {node}<br>"
        node_info += f"Tipo: {G.nodes[node].get('type', 'sensor')}"
        node_text.append(node_info)
        
        if G.nodes[node].get('type') == 'base_station':
            node_color.append('red')
        else:
            node_color.append('blue')


    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        customdata=[(node) for node in G.nodes()], # Adiciona o ID do nó
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                title_side='right'  # Corrigido para title_side
            ),
            line_width=2))
    
    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies
    node_trace.marker.size = [s * 2 for s in node_adjacencies]


    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title=dict(text='<br>Topologia da Rede Interativa', font=dict(size=16)),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

def plotar_metricas(metrics):
    """
    Cria e retorna uma figura Matplotlib com as métricas da simulação.
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
