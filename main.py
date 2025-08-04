from network_generator import (
    criar_grafo_rssf,
    criar_grafo_aleatorio,
    criar_grafo_barabasi_albert,
    criar_grafo_watts_strogatz
)
from simulation import executar_simulacao
from visualization import plotar_rede, plotar_metricas

def main():
    """Função principal para executar a simulação de RSSF."""
    # --- CONFIGURAÇÃO DA SIMULAÇÃO ---
    # Altere os parâmetros aqui para diferentes simulações
    params = {
        'tipo_rede': '1',  # 1:RSSF, 2:Aleatória, 3:Barabási-Albert, 4:Watts-Strogatz
        'num_nos': 100,
        'tam_area': 100,
        'tempo_simulacao': 100,

        # Parâmetros para RSSF
        'raio_comunicacao': 20,
        'num_estacoes_base': 2,

        # Parâmetros para Rede Aleatória
        'p_conexao': 0.1,

        # Parâmetros para Barabási-Albert
        'm_conexoes': 3,

        # Parâmetros para Watts-Strogatz
        'k_vizinhos': 4,
        'p_reconectar': 0.1
    }

    print("--- Configuração da Simulação ---")
    print(f"Tipo de Rede: {params['tipo_rede']}")
    print(f"Número de Nós: {params['num_nos']}")

    # 1. Cria o grafo com base na escolha do usuário
    G = None
    if params['tipo_rede'] == '1':
        print("Criando rede RSSF...")
        G = criar_grafo_rssf(
            num_nos=params['num_nos'],
            tam_area=params['tam_area'],
            raio_comunicacao=params['raio_comunicacao'],
            num_estacoes_base=params['num_estacoes_base']
        )
    elif params['tipo_rede'] == '2':
        print("Criando rede Aleatória...")
        G = criar_grafo_aleatorio(
            num_nos=params['num_nos'],
            p_conexao=params['p_conexao'],
            tam_area=params['tam_area']
        )
    elif params['tipo_rede'] == '3':
        print("Criando rede Barabási-Albert...")
        G = criar_grafo_barabasi_albert(
            num_nos=params['num_nos'],
            m_conexoes=params['m_conexoes'],
            tam_area=params['tam_area']
        )
    elif params['tipo_rede'] == '4':
        print("Criando rede Watts-Strogatz...")
        G = criar_grafo_watts_strogatz(
            num_nos=params['num_nos'],
            k_vizinhos=params['k_vizinhos'],
            p_reconectar=params['p_reconectar'],
            tam_area=params['tam_area']
        )

    if G is None:
        print("Erro ao criar o grafo. Verifique os parâmetros.")
        return

    # 2. Executa a simulação
    print("\nExecutando a simulação...")
    metricas = executar_simulacao(G, params['tempo_simulacao'])

    # 3. Imprime as métricas de desempenho
    print("\n--- Resultados da Simulação ---")
    if metricas['pacotes_gerados'] > 0:
        taxa_de_entrega = (metricas['pacotes_entregues'] / metricas['pacotes_gerados']) * 100
        print(f"Taxa de Entrega de Pacotes: {taxa_de_entrega:.2f}%")
    else:
        print("Nenhum pacote foi gerado na simulação (verifique se há estações base).")

    if metricas['latencias']:
        latencia_media = sum(metricas['latencias']) / len(metricas['latencias'])
        print(f"Latência Média: {latencia_media:.2f} unidades de tempo")

    if metricas['contagens_de_saltos']:
        media_saltos = sum(metricas['contagens_de_saltos']) / len(metricas['contagens_de_saltos'])
        print(f"Média de Saltos: {media_saltos:.2f}")

    print(f"\n--- Metricas da Rede ---")
    if not metricas['is_connected']:
        print("Aviso: A rede não está totalmente conectada.")
        print(f"Diâmetro do Maior Componente Conectado: {metricas['diametro_rede']}")
    else:
        print(f"Diâmetro da Rede: {metricas['diametro_rede']}")

    if metricas['contagens_de_encaminhamento']:
        print("\n--- Nós de Gargalo ---")
        gargalos = sorted(metricas['contagens_de_encaminhamento'].items(), key=lambda x: x[1], reverse=True)[:5]
        for no, contagem in gargalos:
            print(f"Nó {no}: {contagem} encaminhamentos")

    print("\n--- Top 5 Nós por Centralidade de Grau ---")
    centralidade_grau = sorted(metricas['centralidade_de_grau'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, centralidade in centralidade_grau:
        print(f"Nó {no}: {centralidade:.4f}")

    print("\n--- Top 5 Nós por Centralidade de Intermediação (Pontes) ---")
    centralidade_intermediacao = sorted(metricas['centralidade_de_intermediacao'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, centralidade in centralidade_intermediacao:
        print(f"Nó {no}: {centralidade:.4f}")

    print("\n--- Top 5 Nós por Centralidade de Proximidade ---")
    centralidade_proximidade = sorted(metricas['centralidade_de_proximidade'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, centralidade in centralidade_proximidade:
        print(f"Nó {no}: {centralidade:.4f}")

    print("\n--- Top 5 Nós por Centralidade de Autovetor (Influência) ---")
    centralidade_autovetor = sorted(metricas['centralidade_de_autovetor'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, centralidade in centralidade_autovetor:
        print(f"Nó {no}: {centralidade:.4f}")

    print("\n--- Top 5 Nós por Coeficiente de Agrupamento (Cluster) ---")
    centralidade_clique = sorted(metricas['centralidade_de_clique'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, centralidade in centralidade_clique:
        print(f"Nó {no}: {centralidade:.4f}")

    print("\n--- Top 5 Nós por PageRank ---")
    centralidade_pagerank = sorted(metricas['centralidade_de_pagerank'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, centralidade in centralidade_pagerank:
        print(f"Nó {no}: {centralidade:.4f}")

    # 4. Visualiza os resultados
    print("\nGerando visualizações...")
    plotar_rede(G)
    plotar_metricas(metricas)
    print("Simulação concluída. Verifique os gráficos gerados.")

if __name__ == "__main__":
    main()
