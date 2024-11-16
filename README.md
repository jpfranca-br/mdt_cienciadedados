### PUC RIO - MDT - Ciência de Dados - Grupo 3

#### **Descrição do Projeto**
Este projeto foi desenvolvido como parte do trabalho final para a disciplina "Ciência de Dados Para Transformação Digital" no curso de pós-graduação em Transformação Digital da PUC-Rio, orientado pelo Professor Dr. Dan Reznik. O objetivo é realizar uma análise de dados para entender a relação entre fatores econômicos e o volume de visitantes de diferentes regiões, usando técnicas de análise, transformação, enriquecimento e visualização de dados.

Os gráficos interativos gerados podem ser vistos em [https://mdt-cienciadedados.surge.sh/](https://mdt-cienciadedados.surge.sh/)

---

#### **Funcionalidades Principais**

##### **Carregamento e Limpeza de Dados**
1. **`load_csv_files()`**
   - Carrega os arquivos CSV originais (`viagens.csv` e `indicators.csv`), realizando a limpeza inicial de espaços em branco e removendo acentuações dos nomes de países para garantir uniformidade nos dados.

2. **`create_or_load_country_match()`**
   - Gera ou carrega uma tabela de correspondência (`country_match.csv`) para alinhar os nomes dos países entre os dados de viagens e indicadores, com feedback claro ao usuário em caso de erros.

---

##### **Transformação e Enriquecimento**
1. **`merge_data()`**
   - Realiza a fusão dos dados de `viagens` e `indicators` com base na tabela de correspondência de países.
   - Adiciona colunas calculadas, como:
     - `travels_per_capita`: Viagens per capita.
     - `travels_per_1000_people`: Viagens por mil habitantes.
   - Mostra o número total de países correspondidos.

---

##### **Profiling e Análise de Dados**
1. **`data_profiling()`**
   - Gera um relatório detalhado com:
     - Estrutura dos dados.
     - Primeiras linhas.
     - Valores nulos.
     - Descrição estatística.
   - Salvo como `profiling_report.txt`.

2. **`correlation()`**
   - Calcula e salva métricas de correlação entre o número de visitantes e o GNI per capita por região e ano.
   - Salva a tabela resumo das métricas como `correlation.csv`.

---

##### **Visualizações Gráficas**
As visualizações são salvas em formato PNG e HTML interativo na pasta `images/` e podem ser abertas automaticamente no navegador.

1. **Matriz de Correlação (`correlation_matrix()`)**
   - Gera uma matriz de correlação animada ano a ano, destacando a relação entre variáveis numéricas.

2. **Gráfico Radar (`radar()`)**
   - Apresenta o GNI per capita, o total de visitantes e a população por região, permitindo a visualização de tendências comparativas.

3. **Gráfico de Barras Empilhadas (`stack_percent()`)**
   - Exibe a distribuição percentual dos tipos de transporte (marítimo e aéreo) por ano, com animação por região de origem.

4. **Gráfico de Bolhas (`bubble()`)**
   - Mostra o volume de visitantes em relação ao GNI per capita e à população, ajudando a identificar correlações econômicas.

5. **Boxplots (`boxplot_h()` e `boxplot_v()`)**
   - Apresentam a dispersão dos visitantes por região e país de origem, identificando outliers e variações.

6. **Mapa de Bolhas Global (`worldmap_bubble()`)**
   - Exibe o número de visitantes por país de origem em um mapa mundial.

---

#### **Novos Recursos**
1. **Automação de Instalação de Dependências (`install_dependencies.py`)**
   - Instala automaticamente bibliotecas essenciais, como `pandas`, `numpy`, e `plotly`.

2. **Publicação de Gráficos com Surge (`save_images_to_static_website_using_surge.py`)**
   - Automatiza a publicação dos gráficos em uma página web estática hospedada pelo Surge.
   - Gera um arquivo `index.html` com links para os gráficos interativos.

---

#### **Arquivos de Saída**
1. **`merged_viagens_indicators.csv`:** Dados fundidos e enriquecidos.
2. **`profiling_report.txt`:** Relatório de profiling detalhado.
3. **`correlation.csv`:** Métricas de correlação entre viagens e GNI.
4. **Diretório `images/`:** Contém gráficos PNG e HTML interativos prontos para visualização.

Este projeto oferece uma análise robusta e ferramentas práticas para transformar dados brutos em insights visuais e métricas acionáveis.
