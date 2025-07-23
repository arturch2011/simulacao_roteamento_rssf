# Simulação de Roteamento em Redes de Sensores Sem Fio (RSSF)

Este projeto fornece uma simulação para análise de desempenho de um protocolo de roteamento em Redes de Sensores Sem Fio (RSSF). A simulação modela uma rede de sensores que se comunicam com uma estação base e utiliza um protocolo de inundação (flooding) para o envio de pacotes.

## Funcionalidades

- **Geração de Topologia de Rede**: Cria uma rede de sensores sem fio com um número customizável de nós, área de cobertura e raio de comunicação.
- **Simulação de Roteamento**: Simula o envio de pacotes de dados dos nós sensores para a estação base utilizando um protocolo de roteamento por inundação.
- **Análise de Desempenho**: Coleta e exibe métricas de desempenho da rede, como:
    - Taxa de Entrega de Pacotes
    - Latência Média
    - Média de Saltos por Pacote
    - Identificação de Nós de Gargalo (nós que mais encaminham pacotes)
- **Visualização de Dados**: Gera gráficos para visualizar a topologia da rede e as métricas de desempenho.

## Tecnologias Utilizadas

- **Python 3**: Linguagem de programação principal.
- **SimPy**: Biblioteca para simulação de eventos discretos.
- **NetworkX**: Biblioteca para criação, manipulação e estudo da estrutura, dinâmica e funções de redes complexas.
- **Matplotlib**: Biblioteca para criação de visualizações estáticas, animadas e interativas em Python.

## Como Usar

### Pré-requisitos

- Python 3.x
- Pip (gerenciador de pacotes do Python)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/simulacao_roteamento_rssf.git
   cd simulacao_roteamento_rssf
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Executando a Simulação

Para executar a simulação com os parâmetros padrão, basta executar o script `main.py`:

```bash
python main.py
```

Após a execução, os resultados da simulação serão exibidos no console e os gráficos de visualização serão mostrados em janelas separadas.

### Customizando a Simulação

Você pode alterar os parâmetros da simulação diretamente no arquivo `main.py`:

- `NUM_NOS`: Número de nós sensores na rede.
- `TAMANHO_AREA`: O tamanho da área quadrada onde os nós estão distribuídos.
- `RAIO_COMUNICACAO`: O raio de comunicação de cada nó.
- `TEMPO_SIMULACAO`: O tempo total da simulação em unidades de tempo.
- `POS_ESTACAO_BASE`: A posição da estação base na área da rede.

## Estrutura do Projeto

- **`main.py`**: O ponto de entrada da aplicação. Orquestra a criação da rede, a execução da simulação e a visualização dos resultados.
- **`network_generator.py`**: Responsável por criar o grafo da rede de sensores sem fio utilizando a biblioteca NetworkX.
- **`simulation.py`**: Contém a lógica da simulação de roteamento utilizando a biblioteca SimPy.
- **`visualization.py`**: Responsável por gerar os gráficos da topologia da rede e das métricas de desempenho utilizando a biblioteca Matplotlib.
- **`requirements.txt`**: Lista as dependências do projeto.
- **`README.md`**: Este arquivo.
