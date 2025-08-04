import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from network_generator import (
    criar_grafo_rssf,
    criar_grafo_aleatorio,
    criar_grafo_barabasi_albert,
    criar_grafo_watts_strogatz
)
from simulation import executar_simulacao
from visualization import plotar_rede, plotar_metricas, plotar_comparacao_betweenness, plotar_metricas_interativo, plotar_comparacao_betweenness_interativo, plotar_rede_com_pontos_criticos

st.set_page_config(layout="wide", page_title="Simulador RSSF")

# Configurações de performance
if 'performance_mode' not in st.session_state:
    st.session_state['performance_mode'] = True  # Modo performance ativado por padrão

st.title("Simulador de Roteamento em Redes Complexas")

# --- Funções Auxiliares ---
@st.cache_data(ttl=300)  # Cache por 5 minutos
def calcular_metricas_cached(grafo_edges, grafo_nodes, tempo_simulacao):
    """Função auxiliar para cache das métricas computacionalmente caras."""
    import networkx as nx
    # Recriar o grafo a partir dos dados
    G = nx.Graph()
    G.add_edges_from(grafo_edges)
    for node, data in grafo_nodes:
        G.add_node(node, **data)
    
    return executar_simulacao(G, tempo_simulacao)

def rodar_simulacao(G, tempo_simulacao):
    """Executa a simulação e armazena os resultados no estado da sessão."""
    with st.spinner("Executando a simulação..."):
        # Converter grafo para formato serializável para cache
        grafo_edges = list(G.edges())
        grafo_nodes = [(node, data) for node, data in G.nodes(data=True)]
        
        metricas = calcular_metricas_cached(grafo_edges, grafo_nodes, tempo_simulacao)
        st.session_state['resultados'] = {
            'G': G,
            'metricas': metricas
        }

# --- Barra Lateral de Configuração ---
st.sidebar.header("Parâmetros da Simulação")

# Controle de performance
with st.sidebar.expander("⚙️ Configurações de Performance"):
    performance_mode = st.checkbox("Modo Performance", value=st.session_state.get('performance_mode', True),
                                 help="Reduz complexidade dos gráficos para melhor performance")
    st.session_state['performance_mode'] = performance_mode
    
    if performance_mode:
        st.info("✅ Gráficos otimizados ativos")
    else:
        st.warning("⚠️ Modo completo pode ser mais lento")
    
    if st.button("🔄 Limpar Cache"):
        st.cache_data.clear()
        st.success("Cache limpo! Recarregue a página se necessário.")

tipo_rede_map = {
    "RSSF (Proximidade)": "rssf",
    "Aleatória (Erdos-Reny)": "aleatoria",
    "Barabási-Albert (Preferential Attachment)": "barabasi_albert",
    "Watts-Strogatz (Small-World)": "watts_strogatz",
}

tipo_rede_selecionado = st.sidebar.selectbox(
    "Selecione o Tipo de Rede",
    options=list(tipo_rede_map.keys())
)

# Parâmetros comuns
num_nos = st.sidebar.slider("Número de Nós", 5, 500, 100)
tam_area = st.sidebar.slider("Tamanho da Área", 50, 200, 100)
num_estacoes_base = st.sidebar.slider("Número de Estações Base", 0, 10, 1)
tempo_simulacao = st.sidebar.slider("Tempo de Simulação", 0, 500, 100)

params = {}

# Parâmetros específicos do tipo de rede
if tipo_rede_map[tipo_rede_selecionado] == 'rssf':
    params['raio_comunicacao'] = st.sidebar.slider("Raio de Comunicação", 5, 50, 20)
elif tipo_rede_map[tipo_rede_selecionado] == 'aleatoria':
    params['p_conexao'] = st.sidebar.slider("Probabilidade de Conexão (p)", 0.0, 1.0, 0.1, 0.01)
elif tipo_rede_map[tipo_rede_selecionado] == 'barabasi_albert':
    params['m_conexoes'] = st.sidebar.slider("Conexões para Novos Nós (m)", 1, 10, 2)
elif tipo_rede_map[tipo_rede_selecionado] == 'watts_strogatz':
    params['k_vizinhos'] = st.sidebar.slider("Número de Vizinhos (k)", 1, 20, 4)
    params['p_reconectar'] = st.sidebar.slider("Probabilidade de Reconexão (p)", 0.0, 1.0, 0.1, 0.01)

# Botão para iniciar a simulação
if st.sidebar.button("Iniciar Nova Simulação"):
    with st.spinner("Criando a rede..."):
        G = None
        tipo_rede = tipo_rede_map[tipo_rede_selecionado]
        
        if tipo_rede == 'rssf':
            G = criar_grafo_rssf(num_nos, tam_area, params['raio_comunicacao'], num_estacoes_base)
        elif tipo_rede == 'aleatoria':
            G = criar_grafo_aleatorio(num_nos, params['p_conexao'], tam_area, num_estacoes_base)
        elif tipo_rede == 'barabasi_albert':
            G = criar_grafo_barabasi_albert(num_nos, params['m_conexoes'], tam_area, num_estacoes_base)
        elif tipo_rede == 'watts_strogatz':
            G = criar_grafo_watts_strogatz(num_nos, params['k_vizinhos'], params['p_reconectar'], tam_area, num_estacoes_base)

        rodar_simulacao(G, tempo_simulacao)
        st.session_state['no_selecionado'] = None # Limpa a seleção de nó

# --- Exibição dos Resultados ---
st.header("Resultados da Simulação")

if 'resultados' in st.session_state:
    resultados = st.session_state['resultados']
    G = resultados['G']
    metricas = resultados['metricas']

    col1, col2 = st.columns([1, 2])

    with col2:
        st.subheader("Visualização da Rede")
        
        # Abas para diferentes visualizações
        tab1, tab2 = st.tabs(["Rede Normal", "Análise de Robustez"])
        
        with tab1:
            fig_rede = plotar_rede(G)
            # Usa plotly_events para capturar cliques
            selected_points = plotly_events(fig_rede, click_event=True, hover_event=False, select_event=False, key="rede_normal")

            if selected_points:
                # Pega o índice do ponto clicado
                point_index = selected_points[0]['pointIndex']
                # Obtém a lista de nós na mesma ordem que no gráfico
                nodes_list = list(G.nodes())
                # Pega o ID do nó usando o índice
                node_id = nodes_list[point_index]
                st.session_state['no_selecionado'] = node_id
        
        with tab2:
            # Só mostrar se houver pontos críticos para evitar processamento desnecessário
            if metricas.get('pontos_articulacao') or metricas.get('pontes'):
                fig_robustez = plotar_rede_com_pontos_criticos(G, metricas)
                st.plotly_chart(fig_robustez, use_container_width=True, key="robustez")
                
                # Informações sobre robustez
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    if metricas.get('pontos_articulacao'):
                        st.error(f"⚠️ {len(metricas['pontos_articulacao'])} pontos críticos encontrados")
                        st.write("**Nós críticos:**", metricas['pontos_articulacao'])
                with col_info2:
                    if metricas.get('pontes'):
                        st.error(f"⚠️ {len(metricas['pontes'])} pontes críticas encontradas")
                        pontes_str = [f"{u}-{v}" for u, v in metricas['pontes']]
                        st.write("**Enlaces críticos:**", pontes_str)
            else:
                st.success("✅ Rede robusta - sem pontos únicos de falha!")
                st.info("Esta rede não possui pontos de articulação ou pontes críticas.")
                
                # Mostrar rede normal se não há pontos críticos
                fig_rede_backup = plotar_rede(G)
                st.plotly_chart(fig_rede_backup, use_container_width=True, key="robustez_backup")


    with col1:
        st.subheader("Métricas de Desempenho")
        if metricas.get('pacotes_gerados', 0) > 0:
            taxa_entrega = (metricas.get('pacotes_entregues', 0) / metricas['pacotes_gerados']) * 100
            st.metric("Taxa de Entrega", f"{taxa_entrega:.2f}%")
            latencia_media = sum(metricas.get('latencias', [0])) / len(metricas.get('latencias', [1]))
            st.metric("Latência Média", f"{latencia_media:.2f}s")
            saltos_medios = sum(metricas.get('contagens_de_saltos', [0])) / len(metricas.get('contagens_de_saltos', [1]))
            st.metric("Média de Saltos", f"{saltos_medios:.2f}")
        else:
            st.info("A simulação de pacotes não foi executada.")
        
        st.subheader("Métricas da Rede")
        
        # Métricas básicas
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Ordem (Nós)", f"{metricas.get('ordem', 'N/A')}")
            st.metric("Tamanho (Arestas)", f"{metricas.get('tamanho', 'N/A')}")
        with col_m2:
            st.metric("Diâmetro da Rede", f"{metricas.get('diametro_rede', 'N/A')}")
            if metricas.get('distancia_media'):
                st.metric("Distância Média", f"{metricas.get('distancia_media', 'N/A'):.2f}")
            else:
                st.metric("Distância Média", "N/A")
        with col_m3:
            if metricas.get('coeficiente_clusterizacao') is not None:
                st.metric("Coef. Clusterização", f"{metricas.get('coeficiente_clusterizacao', 0):.3f}")
            else:
                st.metric("Coef. Clusterização", "N/A")
            if metricas.get('assortatividade') is not None:
                st.metric("Assortatividade", f"{metricas.get('assortatividade', 0):.3f}")
            else:
                st.metric("Assortatividade", "N/A")
        
        # Métricas de comunidade
        col_m4, col_m5 = st.columns(2)
        with col_m4:
            if metricas.get('modularidade') is not None:
                st.metric("Modularidade", f"{metricas.get('modularidade', 0):.3f}")
            else:
                st.metric("Modularidade", "N/A")
        with col_m5:
            st.metric("Nº Comunidades", f"{metricas.get('numero_comunidades', 'N/A')}")
        
        # Métricas de robustez e conectividade
        st.subheader("Métricas de Robustez")
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Edge Connectivity", f"{metricas.get('edge_connectivity', 'N/A')}")
            st.metric("Node Connectivity", f"{metricas.get('node_connectivity', 'N/A')}")
        with col_r2:
            st.metric("Pontos de Articulação", f"{metricas.get('numero_pontos_articulacao', 'N/A')}")
            st.metric("Pontes Críticas", f"{metricas.get('numero_pontes', 'N/A')}")
        with col_r3:
            # Avaliar robustez geral
            if metricas.get('edge_connectivity', 0) >= 2:
                st.success("🟢 Rede Robusta")
            elif metricas.get('edge_connectivity', 0) == 1:
                st.warning("🟡 Rede Vulnerável")
            else:
                st.error("🔴 Rede Fragmentada")
        
        # Mostrar nós críticos se existirem
        if metricas.get('pontos_articulacao'):
            st.warning(f"⚠️ Nós Críticos (Pontos de Articulação): {metricas['pontos_articulacao']}")
        
        if metricas.get('pontes'):
            pontes_str = [f"({u}-{v})" for u, v in metricas['pontes']]
            st.warning(f"⚠️ Arestas Críticas (Pontes): {pontes_str}")
        
        if not metricas.get('is_connected', True):
            st.warning("⚠️ A rede não está totalmente conectada.")
        
        # Explicações das métricas
        with st.expander("📖 Explicação das Métricas de Rede"):
            st.markdown("""
            ### Métricas Fundamentais de Redes de Sensores Sem Fio (RSSF)
            
            **🔢 Ordem e Tamanho:**
            - **Ordem**: Número total de nós (sensores + estações base) na rede
            - **Tamanho**: Número total de conexões (enlaces de comunicação) entre os nós
            - *Relevância*: Determinam a capacidade e complexidade computacional da rede
            
            **📏 Métricas de Distância:**
            - **Diâmetro**: Maior distância (em saltos) entre qualquer par de nós conectados
            - **Distância Média**: Média de todas as distâncias mais curtas entre pares de nós
            - *Relevância*: Afetam diretamente latência e consumo energético nas comunicações
            
            **🔗 Coeficiente de Clusterização:**
            - Mede quão densamente conectados estão os vizinhos de cada nó (0 a 1)
            - *Relevância*: Valores altos indicam redundância de caminhos e maior tolerância a falhas
            
            **🏘️ Modularidade:**
            - Identifica grupos/comunidades de nós densamente conectados (-1 a 1)
            - *Relevância*: Útil para otimização energética através de protocolos hierárquicos
            
            **⚖️ Assortatividade:**
            - Tendência de nós com grau similar se conectarem (-1 a 1)
            - *Positiva*: Nós populares conectam-se entre si (redes sociais)
            - *Negativa*: Nós populares conectam-se a nós com poucos vizinhos (redes tecnológicas)
            - *Relevância*: Influencia robustez contra falhas de nós importantes
            
            **🛡️ Métricas de Robustez:**
            - **Edge Connectivity**: Número mínimo de enlaces que devem falhar para fragmentar a rede
            - **Node Connectivity**: Número mínimo de nós que devem falhar para fragmentar a rede
            - **Pontos de Articulação**: Nós únicos cuja falha desconecta a rede
            - **Pontes**: Enlaces únicos cuja falha desconecta a rede
            - *Relevância*: Critiais para tolerância a falhas e manutenção da conectividade
            
            ### 🎯 Interpretação para RSSF:
            - **Diâmetro baixo**: Comunicação mais rápida e eficiente
            - **Alta clusterização**: Maior redundância e tolerância a falhas
            - **Modularidade alta**: Oportunidades para protocolos de agregação de dados
            - **Assortatividade negativa**: Típica de redes bem distribuídas espacialmente
            - **Alta conectividade**: Rede mais robusta contra falhas de nós/enlaces
            - **Poucos pontos de articulação**: Menor vulnerabilidade a falhas críticas
            """)
        
        # Análise detalhada de robustez
        with st.expander("🛡️ Análise Detalhada de Robustez"):
            st.markdown("""
            ### Interpretação das Métricas de Robustez
            
            **🔗 Edge Connectivity:**
            - **Valor ≥ 2**: Rede robusta, múltiplos caminhos alternativos
            - **Valor = 1**: Rede vulnerável, existe pelo menos uma ponte crítica
            - **Valor = 0**: Rede já fragmentada ou com apenas um nó
            
            **👥 Node Connectivity:**
            - **Valor ≥ 2**: Não há pontos únicos de falha
            - **Valor = 1**: Existe pelo menos um ponto de articulação
            - **Valor = 0**: Rede já fragmentada
            
            **⚠️ Pontos de Articulação:**
            - Nós cuja remoção aumenta o número de componentes conectados
            - Em RSSF: nós críticos para manter conectividade global
            - **Estratégia**: Adicionar redundância ao redor destes nós
            
            **🌉 Pontes:**
            - Enlaces cuja remoção aumenta o número de componentes conectados
            - Em RSSF: enlaces críticos que devem ser protegidos
            - **Estratégia**: Adicionar enlaces alternativos
            
            ### 🎯 Recomendações para RSSF:
            - **Monitorar** pontos de articulação com maior frequência
            - **Backup**: Ter planos de roteamento alternativos
            - **Deployment**: Evitar topologias com muitos pontos críticos
            - **Manutenção**: Priorizar reparo de nós/enlaces críticos
            """)
        

        # --- Interatividade com o Grafo ---
        st.subheader("Nó Selecionado")
        
        no_selecionado = st.session_state.get('no_selecionado')

        if no_selecionado is not None:
            st.write(f"**Informações Detalhadas do Nó {no_selecionado}:**")
            
            # Informações básicas do nó
            node_data = G.nodes[no_selecionado]
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write("**Dados Básicos:**")
                st.json(node_data)
                
                # Métricas básicas do nó
                grau = G.degree(no_selecionado)
                vizinhos = list(G.neighbors(no_selecionado))
                st.metric("Grau do Nó", grau)
                st.write(f"**Vizinhos:** {vizinhos}")
            
            with col_info2:
                st.write("**Métricas de Centralidade:**")
                
                # Métricas de centralidade específicas do nó
                centralidades = {}
                if metricas.get('centralidade_de_grau'):
                    centralidades['Grau'] = f"{metricas['centralidade_de_grau'].get(no_selecionado, 0):.4f}"
                if metricas.get('centralidade_de_intermediacao'):
                    centralidades['Intermediação'] = f"{metricas['centralidade_de_intermediacao'].get(no_selecionado, 0):.4f}"
                if metricas.get('centralidade_de_proximidade'):
                    centralidades['Proximidade'] = f"{metricas['centralidade_de_proximidade'].get(no_selecionado, 0):.4f}"
                if metricas.get('centralidade_de_pagerank'):
                    centralidades['PageRank'] = f"{metricas['centralidade_de_pagerank'].get(no_selecionado, 0):.4f}"
                if metricas.get('centralidade_de_clique'):
                    centralidades['Clustering'] = f"{metricas['centralidade_de_clique'].get(no_selecionado, 0):.4f}"
                
                # Métricas específicas de RSSF
                if metricas.get('betweenness_sensores_para_bases'):
                    centralidades['Betweenness S→B'] = f"{metricas['betweenness_sensores_para_bases'].get(no_selecionado, 0):.4f}"
                if metricas.get('betweenness_bases_para_sensores'):
                    centralidades['Betweenness B→S'] = f"{metricas['betweenness_bases_para_sensores'].get(no_selecionado, 0):.4f}"
                
                # Métricas de simulação
                if metricas.get('contagens_de_encaminhamento'):
                    centralidades['Encaminhamentos'] = f"{metricas['contagens_de_encaminhamento'].get(no_selecionado, 0)}"
                
                # Informações de robustez do nó
                if metricas.get('pontos_articulacao') and no_selecionado in metricas['pontos_articulacao']:
                    st.error("⚠️ **PONTO DE ARTICULAÇÃO** - Nó crítico!")
                    st.write("Remover este nó desconectará a rede.")
                
                for nome, valor in centralidades.items():
                    st.metric(nome, valor)

            if st.button(f"Remover Nó {no_selecionado} e Refazer Simulação"):
                G.remove_node(no_selecionado)
                st.session_state['no_selecionado'] = None # Limpa a seleção
                st.success(f"Nó {no_selecionado} removido.")
                rodar_simulacao(G, tempo_simulacao)
                st.rerun() # Força a atualização da UI
        else:
            st.info("Clique em um nó no grafo para ver suas informações detalhadas.")


    st.subheader("Gráficos Interativos de Métricas da Simulação")
    
    if st.session_state.get('performance_mode', True):
        # Modo otimizado
        fig_metricas_interativo = plotar_metricas_interativo(metricas)
        st.plotly_chart(fig_metricas_interativo, use_container_width=True)
        
        st.subheader("Análise de Betweenness Centrality")
        fig_betweenness_interativo = plotar_comparacao_betweenness_interativo(metricas)
        st.plotly_chart(fig_betweenness_interativo, use_container_width=True)
    else:
        # Modo completo (pode ser mais lento)
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            fig_metricas_interativo = plotar_metricas_interativo(metricas)
            st.plotly_chart(fig_metricas_interativo, use_container_width=True)
        with col_graf2:
            fig_betweenness_interativo = plotar_comparacao_betweenness_interativo(metricas)
            st.plotly_chart(fig_betweenness_interativo, use_container_width=True)
    
    # Gráficos estáticos sempre em expander para não sobrecarregar
    with st.expander("📊 Gráficos Estáticos Detalhados"):
        col_est1, col_est2 = st.columns(2)
        with col_est1:
            st.subheader("Métricas da Simulação")
            fig_metricas = plotar_metricas(metricas)
            st.pyplot(fig_metricas)
        with col_est2:
            st.subheader("Betweenness Centrality")
            fig_betweenness = plotar_comparacao_betweenness(metricas)
            st.pyplot(fig_betweenness)

    st.subheader("Análise de Centralidade e Nós Importantes")
    
    def criar_df_centralidade(metrica, nome_coluna):
        if not metrica:
            return pd.DataFrame(columns=['Nó', nome_coluna])
        df = pd.DataFrame(list(metrica.items()), columns=['Nó', nome_coluna])
        df = df.sort_values(by=nome_coluna, ascending=False).reset_index(drop=True)
        df['Nó'] = df['Nó'].astype(str)
        return df.head(10)

    df_grau = criar_df_centralidade(metricas.get('centralidade_de_grau', {}), 'Centralidade de Grau')
    df_intermediacao = criar_df_centralidade(metricas.get('centralidade_de_intermediacao', {}), 'Centralidade de Intermediação')
    df_proximidade = criar_df_centralidade(metricas.get('centralidade_de_proximidade', {}), 'Centralidade de Proximidade')
    df_gargalos = criar_df_centralidade(metricas.get('contagens_de_encaminhamento', {}), 'Contagem de Encaminhamentos')
    
    # Novas métricas de betweenness específicas para RSSF
    df_betweenness_up = criar_df_centralidade(metricas.get('betweenness_sensores_para_bases', {}), 'Betweenness Sensores→Bases')
    df_betweenness_down = criar_df_centralidade(metricas.get('betweenness_bases_para_sensores', {}), 'Betweenness Bases→Sensores')

    c1, c2 = st.columns(2)
    with c1:
        st.write("**Top 10 - Grau**")
        st.dataframe(df_grau)
        st.write("**Top 10 - Proximidade**")
        st.dataframe(df_proximidade)
        st.write("**Top 10 - Betweenness Sensores→Bases**")
        st.dataframe(df_betweenness_up)
    with c2:
        st.write("**Top 10 - Intermediação (Geral)**")
        st.dataframe(df_intermediacao)
        st.write("**Top 10 - Nós de Gargalo**")
        st.dataframe(df_gargalos)
        st.write("**Top 10 - Betweenness Bases→Sensores**")
        st.dataframe(df_betweenness_down)
    
    # Explicação das métricas de betweenness específicas
    with st.expander("📡 Betweenness Centrality Específico para RSSF"):
        st.markdown("""
        ### Análise de Intermediação Direcionada em RSSF
        
        **📤 Betweenness Sensores → Bases (Upload/Coleta):**
        - Identifica nós críticos no fluxo de dados dos sensores para as estações base
        - Representa o padrão típico de coleta de dados em RSSF
        - Nós com alta pontuação são gargalos críticos para agregação de dados
        - *Impacto*: Falha destes nós pode interromper a coleta de grandes áreas da rede
        
        **📥 Betweenness Bases → Sensores (Download/Comando):**
        - Identifica nós críticos no fluxo de comandos das bases para os sensores
        - Representa disseminação de comandos, atualizações ou consultas
        - Nós importantes para reconfiguração da rede e disseminação de informações
        - *Impacto*: Falha destes nós pode impedir controle remoto de regiões da rede
        
        **🎯 Interpretação Prática:**
        - **Valores altos em Upload**: Nós que agregam dados de muitos sensores
        - **Valores altos em Download**: Nós que distribuem comandos para muitos sensores
        - **Nós com ambos altos**: Pontos críticos bidirecionais (maior risco)
        - **Otimização**: Considere balanceamento de carga ou redundância nestes nós
        """)
    

else:
    st.info("Configure os parâmetros na barra lateral e clique em 'Iniciar Nova Simulação' para ver os resultados.")