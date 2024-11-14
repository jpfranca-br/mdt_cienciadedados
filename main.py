import user_plot_module as p
import pandas as pd
import os
import unidecode
import numpy as np
import io

def load_csv_files():
    """Carrega os arquivos CSV 'viagens' e 'indicators', limpando espaços e normalizando os nomes dos países"""
    print("Loading original CSV files...")
    viagens = pd.read_csv('data/viagens.csv', skipinitialspace=True).apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    viagens['País'] = viagens['País'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    indicators = pd.read_csv('data/indicators.csv', skipinitialspace=True)
    indicators = indicators.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    indicators['Country'] = indicators['Country'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    return viagens, indicators

def create_or_load_country_match(viagens, indicators):
    """Gera ou carrega uma tabela de correspondência de países entre os arquivos 'viagens' e 'indicators'"""
    if not os.path.exists('data/country_match.csv'):
        viagens_countries = sorted(viagens['País'].unique())
        indicators_countries = sorted(indicators['Country'].unique())
        max_length = max(len(viagens_countries), len(indicators_countries))
        viagens_countries += [None] * (max_length - len(viagens_countries))
        indicators_countries += [None] * (max_length - len(indicators_countries))
        country_match_df = pd.DataFrame({
            'viagens_country': viagens_countries,
            'indicators_country': indicators_countries
        })
        country_match_df.to_csv('result/country_match.csv', index=False)
        print("Country match table generated and saved to 'country_match.csv'.")
        exit()
    else:
        country_match_df = pd.read_csv('data/country_match.csv')
        return country_match_df

def merge_data(viagens, indicators, country_match_df):
    """Realiza a fusão dos dados de 'viagens' e 'indicators' utilizando a tabela de correspondência de países"""
    print("Merging viagens and indicators using country match table...")
    # Realiza ajustes de nomes de regiões e converte colunas
    viagens['Ano'] = viagens['Ano'].astype(str).str.strip()
    indicators['Year'] = indicators['Year'].astype(str).str.strip()
    # Renomeia colunas específicas para consistência
    def rename_column(origin, target):
        if origin in indicators.columns:
            indicators.rename(columns={origin: target}, inplace=True)
    rename_column('Gross National Income(GNI) in USD','GNI (USD)')
    merged_data = viagens.merge(country_match_df, how='left', left_on='País', right_on='viagens_country')
    merged_data = merged_data.merge(indicators, how='left', left_on=['indicators_country', 'Ano'], right_on=['Country', 'Year'])
    return merged_data

def main():
    """Função principal para execução do pipeline de análise e visualização dos dados"""
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('result'):
        os.makedirs('result')
    viagens, indicators = load_csv_files()
    country_match_df = create_or_load_country_match(viagens, indicators)
    merged_data = merge_data(viagens, indicators, country_match_df)
    p.correlation_matrix(merged_data)
    p.radar(merged_data)
    p.bubble(merged_data)
    p.boxplot_h(merged_data)
    p.boxplot_v(merged_data)
    p.worldmap_bubble(merged_data)
    p.stack_percent(merged_data)
    print("### Caso algum gráfico não abra, aperte F5 no browser ###")

if __name__ == "__main__":
    main()
