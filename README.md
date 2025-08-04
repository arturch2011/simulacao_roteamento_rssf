# Simulação de Roteamento em Redes de Sensores Sem Fio (RSSF)

Este projeto fornece uma simulação abrangente para análise de desempenho e robustez de protocolos de roteamento em Redes de Sensores Sem Fio (RSSF). A simulação modela diferentes tipos de redes complexas e oferece uma interface web interativa para análise detalhada.

## Funcionalidades

### 🌐 Interface Web Interativa
- **Dashboard Streamlit**: Interface web moderna e intuitiva para configuração e visualização
- **Análise em Tempo Real**: Métricas e gráficos atualizados dinamicamente
- **Interatividade**: Clique em nós para análise detalhada e remoção de elementos da rede

### 🔗 Tipos de Redes Suportadas
- **RSSF (Proximidade)**: Rede baseada em raio de comunicação entre sensores
- **Aleatória (Erdős–Rényi)**: Rede com conexões probabilísticas
- **Barabási-Albert**: Rede livre de escala com crescimento preferencial
- **Watts-Strogatz**: Rede de mundo pequeno (small-world)

### 📊 Análise Completa de Rede
- **Métricas Básicas**: Ordem, tamanho, diâmetro, distância média
- **Centralidade**: Grau, intermediação, proximidade, PageRank, clustering
- **Estrutura**: Coeficiente de clusterização, modularidade, assortatividade
- **Robustez**: Conectividade de nós/arestas, pontos de articulação, pontes críticas
- **RSSF Específico**: Betweenness centrality direcionado (sensores↔bases)

### 🎯 Simulação de Roteamento
- **Protocolo de Inundação**: Simulação de envio de pacotes por flooding
- **Métricas de Desempenho**: Taxa de entrega, latência média, contagem de saltos
- **Identificação de Gargalos**: Análise de nós críticos para o tráfego de dados

### 📈 Visualizações Avançadas
- **Gráficos Interativos**: Visualizações Plotly com zoom, pan e seleção
- **Análise de Robustez**: Destaque visual de pontos críticos e vulnerabilidades
- **Comparação de Métricas**: Gráficos comparativos de centralidade e desempenho

## Tecnologias Utilizadas

- **Python 3**: Linguagem de programação principal
- **Streamlit**: Framework para criação da interface web interativa
- **SimPy**: Biblioteca para simulação de eventos discretos
- **NetworkX**: Biblioteca para análise de redes complexas e grafos
- **Plotly**: Biblioteca para visualizações interativas e dashboards
- **Matplotlib**: Biblioteca para visualizações estáticas complementares
- **Pandas**: Manipulação e análise de dados estruturados

## Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/arturch2011/simulacao_roteamento_rssf.git
   cd simulacao_roteamento_rssf
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Executando a Aplicação

#### Interface Web Interativa (Recomendado)

Para executar a interface web completa com análise interativa:

```bash
python -m streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`.

#### Simulação em Linha de Comando

Para executar uma simulação básica no terminal:

```bash
python main.py
```

### Usando a Interface Web

1. **Configuração de Parâmetros**: Use a barra lateral esquerda para:
   - Selecionar o tipo de rede (RSSF, Aleatória, Barabási-Albert, Watts-Strogatz)
   - Ajustar número de nós, tamanho da área e estações base
   - Definir parâmetros específicos do tipo de rede
   - Configurar tempo de simulação

2. **Executar Simulação**: Clique em "Iniciar Nova Simulação" para:
   - Gerar a topologia da rede
   - Executar a simulação de roteamento
   - Calcular métricas de rede e robustez

3. **Análise Interativa**:
   - **Visualização da Rede**: Explore a topologia e clique em nós para detalhes
   - **Métricas de Robustez**: Identifique pontos críticos e vulnerabilidades
   - **Gráficos Interativos**: Analise métricas de centralidade e desempenho
   - **Remoção de Nós**: Teste a robustez removendo nós específicos

4. **Configurações de Performance**: 
   - Use o modo performance para redes grandes (>200 nós)
   - Limpe o cache se necessário para liberar memória

Após a execução, os resultados da simulação serão exibidos no console e os gráficos de visualização serão mostrados em janelas separadas.

### Customizando a Simulação (Linha de Comando)

Você pode alterar os parâmetros da simulação diretamente no arquivo `main.py`:

- `NUM_NOS`: Número de nós sensores na rede.
- `TAMANHO_AREA`: O tamanho da área quadrada onde os nós estão distribuídos.
- `RAIO_COMUNICACAO`: O raio de comunicação de cada nó.
- `TEMPO_SIMULACAO`: O tempo total da simulação em unidades de tempo.
- `POS_ESTACAO_BASE`: A posição da estação base na área da rede.

## Estrutura do Projeto

- **`app.py`**: Interface web principal usando Streamlit com dashboard interativo completo
- **`main.py`**: Ponto de entrada para simulação em linha de comando (modo básico)
- **`network_generator.py`**: Geração de diferentes tipos de topologias de rede (RSSF, Barabási-Albert, etc.)
- **`simulation.py`**: Motor de simulação com análise de métricas de rede e robustez
- **`visualization.py`**: Módulo de visualização com gráficos interativos Plotly e estáticos Matplotlib
- **`requirements.txt`**: Lista de dependências do projeto
- **`README.md`**: Documentação do projeto (este arquivo)

## Métricas e Análises Disponíveis

### 📊 Métricas de Rede
- **Estruturais**: Ordem, tamanho, diâmetro, distância média
- **Clustering**: Coeficiente de clusterização, modularidade
- **Centralidade**: Grau, intermediação, proximidade, PageRank, clustering local
- **Assortatividade**: Tendência de conexão entre nós similares

### 🛡️ Análise de Robustez
- **Conectividade**: Edge connectivity, node connectivity
- **Pontos Críticos**: Pontos de articulação, pontes críticas
- **Vulnerabilidades**: Identificação de nós/enlaces únicos de falha

### 📡 Específico para RSSF
- **Betweenness Direcionado**: Análise separada para fluxos sensores→bases e bases→sensores
- **Estações Base**: Identificação visual e análise específica
- **Padrões de Tráfego**: Simulação de coleta de dados e disseminação de comandos

### 🚀 Métricas de Desempenho
- **Taxa de Entrega**: Percentual de pacotes entregues com sucesso
- **Latência**: Tempo médio de entrega de pacotes
- **Eficiência**: Número médio de saltos por pacote
- **Gargalos**: Identificação de nós sobrecarregados

## Exemplos de Uso

### Análise de Robustez de RSSF
```bash
# Execute a interface web
python -m streamlit run app.py

# Configure: RSSF com 100 nós, raio 20, 2 estações base
# Analise: Pontos de articulação e conectividade
# Teste: Remova nós críticos e observe o impacto
```

### Comparação de Topologias
```bash
# Execute simulações com diferentes tipos de rede
# Compare métricas de robustez e desempenho
# Identifique a topologia mais adequada para seu cenário
```

## Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

**Arthur Coutinho** - [arturch2011](https://github.com/arturch2011)

---

### 🎯 Dicas de Performance

- **Redes Grandes**: Use o modo performance para redes com >200 nós
- **Cache**: O sistema mantém cache inteligente das simulações
- **Interatividade**: Desative visualizações desnecessárias em redes muito grandes
- **Memória**: Limpe o cache periodicamente em sessões longas
