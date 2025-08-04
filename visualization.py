import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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

    # Separar nós por tipo
    sensor_x, sensor_y, sensor_text, sensor_customdata = [], [], [], []
    base_x, base_y, base_text, base_customdata = [], [], [], []
    sensor_adjacencies = []
    base_adjacencies = []

    # Obter adjacências para calcular tamanho dos nós
    node_adjacencies_dict = {}
    for node, adjacencies in G.adjacency():
        node_adjacencies_dict[node] = len(adjacencies)

    for node in G.nodes():
        x, y = pos[node]
        node_info = f"ID: {node}<br>"
        node_info += f"Tipo: {G.nodes[node].get('type', 'sensor')}"
        
        if G.nodes[node].get('type') == 'base_station':
            base_x.append(x)
            base_y.append(y)
            base_text.append(node_info)
            base_customdata.append(node)
            base_adjacencies.append(node_adjacencies_dict[node])
        else:
            sensor_x.append(x)
            sensor_y.append(y)
            sensor_text.append(node_info)
            sensor_customdata.append(node)
            sensor_adjacencies.append(node_adjacencies_dict[node])

    # Trace para sensores
    sensor_trace = go.Scatter(
        x=sensor_x, y=sensor_y,
        mode='markers',
        hoverinfo='text',
        text=sensor_text,
        name='Sensores',
        customdata=sensor_customdata,
        marker=dict(
            showscale=True,
            colorscale='Blues',
            reversescale=True,
            color=sensor_adjacencies,
            size=[max(8, s * 1.5) for s in sensor_adjacencies],
            colorbar=dict(
                thickness=15,
                title='Conexões do Nó',
                xanchor='left',
                title_side='right'
            ),
            line_width=2))

    # Trace para estações base
    base_trace = go.Scatter(
        x=base_x, y=base_y,
        mode='markers',
        hoverinfo='text',
        text=base_text,
        name='Estações Base',
        customdata=base_customdata,
        marker=dict(
            color='red',
            size=[max(15, s * 2) for s in base_adjacencies] if base_adjacencies else [15],
            symbol='diamond',
            line=dict(width=3, color='darkred')))


    # Criar lista de traces
    traces = [edge_trace, sensor_trace]
    if base_x:  # Adiciona trace das estações base apenas se existirem
        traces.append(base_trace)

    fig = go.Figure(data=traces,
                 layout=go.Layout(
                    title=dict(text='<br>Topologia da Rede Interativa', font=dict(size=16)),
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    ),
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

def plotar_metricas_interativo(metrics):
    """
    Cria gráficos Plotly interativos otimizados com as métricas da simulação.
    """
    # Criar subplots mais simples
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Latência", "Saltos", "Métricas Básicas"),
        specs=[[{"type": "histogram"}, {"type": "histogram"}, {"type": "bar"}]]
    )
    
    # Gráfico de Latência - limitado a 1000 pontos para performance
    if metrics.get('latencias'):
        latencias = metrics['latencias']
        if len(latencias) > 1000:
            import random
            latencias = random.sample(latencias, 1000)
        
        fig.add_trace(
            go.Histogram(x=latencias, name='Latência', 
                        marker_color='skyblue', showlegend=False, nbinsx=20),
            row=1, col=1
        )
    
    # Gráfico de Saltos - limitado a 1000 pontos
    if metrics.get('contagens_de_saltos'):
        saltos = metrics['contagens_de_saltos']
        if len(saltos) > 1000:
            import random
            saltos = random.sample(saltos, 1000)
            
        fig.add_trace(
            go.Histogram(x=saltos, name='Saltos',
                        marker_color='lightgreen', showlegend=False, nbinsx=15),
            row=1, col=2
        )
    
    # Métricas de Rede básicas
    metricas_nomes = []
    valores = []
    
    for nome, chave in [('Ordem', 'ordem'), ('Tamanho', 'tamanho'), 
                       ('Diâmetro', 'diametro_rede'), ('Comunidades', 'numero_comunidades')]:
        if metrics.get(chave) and metrics[chave] != float('inf'):
            metricas_nomes.append(nome)
            valores.append(metrics[chave])
    
    if metricas_nomes:
        fig.add_trace(
            go.Bar(x=metricas_nomes, y=valores, name='Métricas',
                  marker_color='lightcoral', showlegend=False),
            row=1, col=3
        )
    
    # Layout otimizado
    fig.update_layout(
        title_text="Métricas da Simulação",
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def plotar_comparacao_betweenness(metrics):
    """
    Cria e retorna uma figura Matplotlib comparando diferentes métricas de betweenness centrality.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Betweenness geral
    if metrics.get('centralidade_de_intermediacao'):
        betweenness_geral = metrics['centralidade_de_intermediacao']
        top_geral = sorted(betweenness_geral.items(), key=lambda x: x[1], reverse=True)[:10]
        if top_geral:
            nos, valores = zip(*top_geral)
            str_nos = [str(n) for n in nos]
            axes[0].bar(str_nos, valores, color='lightblue', alpha=0.8)
            axes[0].set_title("Betweenness Centrality Geral")
            axes[0].set_xlabel("Nó")
            axes[0].set_ylabel("Centralidade")
            axes[0].tick_params(axis='x', rotation=45)
    
    # Betweenness sensores para bases
    if metrics.get('betweenness_sensores_para_bases'):
        betweenness_up = metrics['betweenness_sensores_para_bases']
        top_up = sorted(betweenness_up.items(), key=lambda x: x[1], reverse=True)[:10]
        if top_up:
            nos, valores = zip(*top_up)
            str_nos = [str(n) for n in nos]
            axes[1].bar(str_nos, valores, color='lightgreen', alpha=0.8)
            axes[1].set_title("Betweenness Sensores → Bases")
            axes[1].set_xlabel("Nó")
            axes[1].set_ylabel("Centralidade")
            axes[1].tick_params(axis='x', rotation=45)
    
    # Betweenness bases para sensores  
    if metrics.get('betweenness_bases_para_sensores'):
        betweenness_down = metrics['betweenness_bases_para_sensores']
        top_down = sorted(betweenness_down.items(), key=lambda x: x[1], reverse=True)[:10]
        if top_down:
            nos, valores = zip(*top_down)
            str_nos = [str(n) for n in nos]
            axes[2].bar(str_nos, valores, color='lightcoral', alpha=0.8)
            axes[2].set_title("Betweenness Bases → Sensores")
            axes[2].set_xlabel("Nó")
            axes[2].set_ylabel("Centralidade")
            axes[2].tick_params(axis='x', rotation=45)
    
    # Configurar subplots vazios se não houver dados
    for i, ax in enumerate(axes):
        if not ax.get_children():
            ax.text(0.5, 0.5, 'Sem dados suficientes', ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    return fig

def plotar_comparacao_betweenness_interativo(metrics):
    """
    Cria gráficos Plotly otimizados comparando betweenness centrality.
    """
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Geral", "Sensores→Bases", "Bases→Sensores")
    )
    
    # Função auxiliar para pegar top 5 (reduzido para performance)
    def get_top_items(data, n=5):
        if not data:
            return [], []
        top_items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
        return [str(x[0]) for x in top_items], [x[1] for x in top_items]
    
    # Betweenness geral
    nos, valores = get_top_items(metrics.get('centralidade_de_intermediacao', {}))
    if nos:
        fig.add_trace(
            go.Bar(x=nos, y=valores, marker_color='lightblue', showlegend=False),
            row=1, col=1
        )
    
    # Sensores para bases
    nos, valores = get_top_items(metrics.get('betweenness_sensores_para_bases', {}))
    if nos:
        fig.add_trace(
            go.Bar(x=nos, y=valores, marker_color='lightgreen', showlegend=False),
            row=1, col=2
        )
    
    # Bases para sensores
    nos, valores = get_top_items(metrics.get('betweenness_bases_para_sensores', {}))
    if nos:
        fig.add_trace(
            go.Bar(x=nos, y=valores, marker_color='lightcoral', showlegend=False),
            row=1, col=3
        )
    
    fig.update_layout(
        title_text="Comparação de Betweenness Centrality (Top 5)",
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def plotar_rede_com_pontos_criticos(G, metricas):
    """
    Cria uma visualização otimizada da rede destacando pontos de articulação.
    """
    pos = nx.get_node_attributes(G, 'pos')
    pontos_articulacao = set(metricas.get('pontos_articulacao', []))
    
    # Arestas - simplificadas
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Separar nós em apenas 3 categorias para simplificar
    normal_x, normal_y, normal_text = [], [], []
    base_x, base_y, base_text = [], [], []
    critico_x, critico_y, critico_text = [], [], []

    for node in G.nodes():
        x, y = pos[node]
        grau = G.degree(node)
        node_info = f"ID: {node}<br>Grau: {grau}"
        
        is_base = G.nodes[node].get('type') == 'base_station'
        is_critical = node in pontos_articulacao
        
        if is_critical:
            node_info += "<br><b>⚠️ CRÍTICO</b>"
            critico_x.append(x)
            critico_y.append(y)
            critico_text.append(node_info)
        elif is_base:
            base_x.append(x)
            base_y.append(y)
            base_text.append(node_info)
        else:
            normal_x.append(x)
            normal_y.append(y)
            normal_text.append(node_info)

    traces = [
        # Arestas
        go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
    ]
    
    # Nós normais
    if normal_x:
        traces.append(go.Scatter(
            x=normal_x, y=normal_y,
            mode='markers',
            hoverinfo='text',
            text=normal_text,
            name='Sensores',
            marker=dict(color='lightblue', size=8)
        ))

    # Estações base
    if base_x:
        traces.append(go.Scatter(
            x=base_x, y=base_y,
            mode='markers',
            hoverinfo='text',
            text=base_text,
            name='Estações Base',
            marker=dict(color='blue', size=12, symbol='diamond')
        ))

    # Pontos críticos
    if critico_x:
        traces.append(go.Scatter(
            x=critico_x, y=critico_y,
            mode='markers',
            hoverinfo='text',
            text=critico_text,
            name='Pontos Críticos',
            marker=dict(color='red', size=15, symbol='star')
        ))

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title='Análise de Robustez - Pontos Críticos',
            showlegend=True,
            hovermode='closest',
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=400
        )
    )
    
    return fig
