
from network_generator import criar_grafo_rssf
from simulation import executar_simulacao
from visualization import plotar_rede, plotar_metricas

# Parâmetros da Simulação
NUM_NOS = 100
TAMANHO_AREA = 100
RAIO_COMUNICACAO = 20
TEMPO_SIMULACAO = 100
POS_ESTACAO_BASE = (50, 50)

def main():
    """Função principal para executar a simulação de RSSF."""
    # 1. Cria o grafo da RSSF
    G = criar_grafo_rssf(
        num_nos=NUM_NOS, 
        tam_area=TAMANHO_AREA, 
        raio_comunicacao=RAIO_COMUNICACAO, 
        pos_estacao_base=POS_ESTACAO_BASE
    )

    # 2. Executa a simulação
    metricas = executar_simulacao(G, TEMPO_SIMULACAO)

    # 3. Imprime as métricas de desempenho
    print("--- Resultados da Simulação ---")
    taxa_de_entrega = (metricas['pacotes_entregues'] / metricas['pacotes_gerados']) * 100
    print(f"Taxa de Entrega de Pacotes: {taxa_de_entrega:.2f}%")
    
    latencia_media = sum(metricas['latencias']) / len(metricas['latencias'])
    print(f"Latência Média: {latencia_media:.2f} unidades de tempo")

    media_saltos = sum(metricas['contagens_de_saltos']) / len(metricas['contagens_de_saltos'])
    print(f"Média de Saltos: {media_saltos:.2f}")

    print("\n--- Nós de Gargalo ---")
    gargalos = sorted(metricas['contagens_de_encaminhamento'].items(), key=lambda x: x[1], reverse=True)[:5]
    for no, contagem in gargalos:
        print(f"Nó {no}: {contagem} encaminhamentos")

    # 4. Visualiza os resultados
    plotar_rede(G)
    plotar_metricas(metricas)

if __name__ == "__main__":
    main()
