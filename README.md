#  PUC RIO - MDT - Ciência de Dados - Grupo 3

## Descrição do Projeto

Este projeto foi desenvolvido como parte do trabalho final para a disciplina "Ciência de Dados Para Transformação Digital" no curso de pós-graduação em Transformação Digital da PUC-Rio, orientado pelo Professor Dr. Dan Reznik. O objetivo é realizar uma análise de dados para entender a relação entre fatores econômicos e o volume de visitantes de diferentes regiões, usando técnicas de análise, transformação, enriquecimento e visualização de dados.

## Funcionalidades Principais

### Carregamento e Limpeza de Dados

1. **Função `load_csv_files()`**  
   Carrega os arquivos CSV originais `viagens.csv` e `indicators.csv`, realizando a limpeza inicial de espaços em branco e removendo acentuações dos nomes de países para garantir uniformidade nos dados.

2. **Função `create_or_load_country_match()`**  
   Gera ou carrega uma tabela de correspondência (`country_match.csv`) para alinhar os nomes dos países entre os dados de `viagens` e `indicators`.

### Transformação e Enriquecimento

1. **Função `merge_data()`**  
   Realiza a fusão dos dados de `viagens` e `indicators` com base na tabela de correspondência de países. Adiciona colunas calculadas, como `travels_per_capita` (viagens per capita) e `travels_per_1000_people` (viagens por mil habitantes), para enriquecer a análise. As variáveis são padronizadas para uniformidade.

### Profiling e Análise de Dados

1. **Função `show_data_profiling()`**  
   Gera um relatório de *profiling* simplificado com estrutura dos dados, primeiras linhas, valores nulos e descrição estatística, salvo como `profiling_report.txt`.

2. **Função `display_and_save_metrics()`**  
   Calcula métricas de correlação entre o número de visitantes e o GNI per capita por região e ano. Salva uma tabela resumo das métricas de correlação em `travel_x_GNI_correlation.csv`.

### Visualizações Gráficas

Cada visualização gera uma imagem no formato PNG e um arquivo HTML interativo na pasta `images`.

1. **Matriz de Correlação (`correlation_matrix()`)**  
   Gera uma matriz de correlação animada ano a ano, destacando a relação entre variáveis numéricas nos dados.

2. **Gráfico Radar (`radar()`)**  
   Apresenta o GNI per capita, o total de visitantes e a população por região, permitindo a visualização de tendências comparativas ano a ano.

3. **Gráfico de Barras Empilhadas por Percentual (`stack_percent()`)**  
   Exibe a distribuição percentual dos tipos de transporte (marítimo e aéreo) por ano, com animação por região de origem, ajudando a entender mudanças na preferência de transporte ao longo do tempo.

4. **Gráfico de Bolhas (`bubble()`)**  
   Mostra o volume de visitantes em relação ao GNI per capita e à população, em escala logarítmica, para identificar correlações entre o nível econômico e o volume de visitantes.

5. **Boxplots Horizontais e Verticais (`boxplot_h()` e `boxplot_v()`)**  
   Apresentam a dispersão dos visitantes por região e país de origem, identificando outliers e variações regionais em cada ano.

6. **Mapa de Bolhas Global (`worldmap_bubble()`)**  
   Exibe o número de visitantes por país de origem em um mapa mundial, facilitando a identificação das regiões com maior volume de turistas.

## Arquivos de Saída

- `merged_viagens_indicators.csv`: Dados fundidos e enriquecidos.
- `profiling_report.txt`: Relatório de *profiling* dos dados.
- `travel_x_GNI_correlation.csv`: Métricas de correlação entre viagens e GNI.
- Diretório `images/`: Contém gráficos PNG e HTML interativos.
