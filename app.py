
import streamlit as st
import pandas as pd
from network_generator import (
    criar_grafo_rssf,
    criar_grafo_aleatorio,
    criar_grafo_barabasi_albert,
    criar_grafo_watts_strogatz
)
from simulation import executar_simulacao
from visualization import plotar_rede, plotar_metricas

st.set_page_config(layout="wide")

st.title("Simulador de Roteamento em Redes Complexas")

# --- Barra Lateral de Configuração ---
st.sidebar.header("Parâmetros da Simulação")

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
tempo_simulacao = st.sidebar.slider("Tempo de Simulação", 10, 500, 100)

params = {}

# Parâmetros específicos do tipo de rede
if tipo_rede_map[tipo_rede_selecionado] == 'rssf':
    params['raio_comunicacao'] = st.sidebar.slider("Raio de Comunicação", 5, 50, 20)
    params['num_estacoes_base'] = st.sidebar.slider("Número de Estações Base", 0, 10, 1)
elif tipo_rede_map[tipo_rede_selecionado] == 'aleatoria':
    params['p_conexao'] = st.sidebar.slider("Probabilidade de Conexão (p)", 0.0, 1.0, 0.1, 0.01)
elif tipo_rede_map[tipo_rede_selecionado] == 'barabasi_albert':
    params['m_conexoes'] = st.sidebar.slider("Conexões para Novos Nós (m)", 1, 10, 2)
elif tipo_rede_map[tipo_rede_selecionado] == 'watts_strogatz':
    params['k_vizinhos'] = st.sidebar.slider("Número de Vizinhos (k)", 1, 20, 4)
    params['p_reconectar'] = st.sidebar.slider("Probabilidade de Reconexão (p)", 0.0, 1.0, 0.1, 0.01)

# Botão para iniciar a simulação
if st.sidebar.button("Iniciar Simulação"):
    with st.spinner("Criando a rede e executando a simulação..."):
        # 1. Cria o grafo
        G = None
        tipo_rede = tipo_rede_map[tipo_rede_selecionado]
        
        if tipo_rede == 'rssf':
            G = criar_grafo_rssf(num_nos, tam_area, params['raio_comunicacao'], params['num_estacoes_base'])
        elif tipo_rede == 'aleatoria':
            G = criar_grafo_aleatorio(num_nos, params['p_conexao'], tam_area)
        elif tipo_rede == 'barabasi_albert':
            G = criar_grafo_barabasi_albert(num_nos, params['m_conexoes'], tam_area)
        elif tipo_rede == 'watts_strogatz':
            G = criar_grafo_watts_strogatz(num_nos, params['k_vizinhos'], params['p_reconectar'], tam_area)

        # 2. Executa a simulação
        metricas = executar_simulacao(G, tempo_simulacao)
        
        # Armazena os resultados no estado da sessão
        st.session_state['resultados'] = {
            'G': G,
            'metricas': metricas
        }

# --- Exibição dos Resultados ---
st.header("Resultados da Simulação")

if 'resultados' in st.session_state:
    resultados = st.session_state['resultados']
    G = resultados['G']
    metricas = resultados['metricas']

    # Colunas para métricas principais e topologia
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Métricas de Desempenho")
        
        taxa_entrega = (metricas['pacotes_entregues'] / metricas['pacotes_gerados']) * 100 if metricas['pacotes_gerados'] > 0 else 0
        st.metric("Taxa de Entrega", f"{taxa_entrega:.2f}%")

        latencia_media = sum(metricas['latencias']) / len(metricas['latencias']) if metricas['latencias'] else 0
        st.metric("Latência Média", f"{latencia_media:.2f}s")

        saltos_medios = sum(metricas['contagens_de_saltos']) / len(metricas['contagens_de_saltos']) if metricas['contagens_de_saltos'] else 0
        st.metric("Média de Saltos", f"{saltos_medios:.2f}")
        
        st.subheader("Métricas da Rede")
        st.metric("Diâmetro da Rede", f"{metricas['diametro_rede']}")
        if not metricas['is_connected']:
            st.warning("A rede não está totalmente conectada.")

    with col2:
        st.subheader("Visualização da Rede")
        fig_rede = plotar_rede(G)
        st.pyplot(fig_rede)

    st.subheader("Gráficos de Métricas da Simulação")
    fig_metricas = plotar_metricas(metricas)
    st.pyplot(fig_metricas)

    st.subheader("Análise de Centralidade e Nós Importantes")
    
    # Prepara os dados para as tabelas
    def criar_df_centralidade(metrica, nome_coluna):
        if not metrica:
            return pd.DataFrame(columns=['Nó', nome_coluna])
        df = pd.DataFrame(list(metrica.items()), columns=['Nó', nome_coluna])
        df = df.sort_values(by=nome_coluna, ascending=False).reset_index(drop=True)
        df['Nó'] = df['Nó'].astype(str)
        return df.head(10)

    df_grau = criar_df_centralidade(metricas['centralidade_de_grau'], 'Centralidade de Grau')
    df_intermediacao = criar_df_centralidade(metricas['centralidade_de_intermediacao'], 'Centralidade de Intermediação')
    df_proximidade = criar_df_centralidade(metricas['centralidade_de_proximidade'], 'Centralidade de Proximidade')
    df_gargalos = criar_df_centralidade(metricas['contagens_de_encaminhamento'], 'Contagem de Encaminhamentos')

    c1, c2 = st.columns(2)
    with c1:
        st.write("**Top 10 - Grau**")
        st.dataframe(df_grau)
        st.write("**Top 10 - Proximidade**")
        st.dataframe(df_proximidade)
    with c2:
        st.write("**Top 10 - Intermediação (Pontes)**")
        st.dataframe(df_intermediacao)
        st.write("**Top 10 - Nós de Gargalo**")
        st.dataframe(df_gargalos)

else:
    st.info("Configure os parâmetros na barra lateral e clique em 'Iniciar Simulação' para ver os resultados.")
