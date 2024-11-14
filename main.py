import user_plot_module as p
import pandas as pd
import os
import unidecode
import numpy as np
import io

# Load the original CSV files
def load_csv_files():
    print("Loading original CSV files...")

    viagens = pd.read_csv('data/viagens.csv', skipinitialspace=True).apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    viagens['País'] = viagens['País'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    indicators = pd.read_csv('data/indicators.csv', skipinitialspace=True)
    indicators.columns = indicators.columns.str.strip()
    indicators = indicators.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    indicators['Country'] = indicators['Country'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    print("CSV files loaded successfully.")
    return viagens, indicators

# Create or load the country match table
def create_or_load_country_match(viagens, indicators):
    print("Generating or loading country match table...")
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
        print("Country match table generated and saved to 'country_match.csv'. Please fill in the appropriate matches.")
        exit()
    else:
        country_match_df = pd.read_csv('data/country_match.csv')
        print("Loaded existing country match table from 'country_match.csv'.")
    return country_match_df

# Merge viagens and indicators using country match table
def merge_data(viagens, indicators, country_match_df):
    # Merges viagens and indicators dataframes, adding travels per capita and travels per 1000 people columns
    print("Merging viagens and indicators using country match table...")
    viagens['Ano'] = viagens['Ano'].astype(str).str.strip()
    indicators['Year'] = indicators['Year'].astype(str).str.strip()
    # Update region names for the year 2006
    viagens.loc[(viagens['Ano'] == '2006') & (viagens['Região'] == 'América Central'), 'Região'] = 'Am Central e Caribe'
    viagens.loc[(viagens['Região'] == 'América Central e Caribe'), 'Região'] = 'Am Central e Caribe'
    viagens.loc[(viagens['Ano'] == '2006') & (viagens['Região'] == 'Oriente Médio'), 'Região'] = 'Ásia'
    # Simplify some columns names
    def rename_column(origin, target):
        if origin in indicators.columns:
            indicators.rename(columns={origin: target}, inplace=True)
    rename_column('Gross National Income(GNI) in USD','GNI (USD)')
    rename_column('Household consumption expenditure (including Non-profit institutions serving households)','Household consumption')
    rename_column('Gross fixed capital formation (including Acquisitions less disposals of valuables)','Gross fixed capital formation')
    rename_column('Wholesale, retail trade, restaurants and hotels (ISIC G-H)','Wholesale, retail, restaurants, hotels')
    rename_column('Agriculture, hunting, forestry, fishing (ISIC A-B)','Agric, hunt, forest, fish (ISIC A-B)')
    rename_column('General government final consumption expenditure','General gov final consumption expenditure')
    rename_column('Transport, storage and communication (ISIC I)','Transport, storage and comms (ISIC I)')
    # Merge
    merged_data = viagens.merge(country_match_df, how='left', left_on='País', right_on='viagens_country')
    merged_data = merged_data.merge(indicators, how='left', left_on=['indicators_country', 'Ano'], right_on=['Country', 'Year'])
    # Calculate travels per capita / per 1000 people
    merged_data['travels_per_capita'] = merged_data.apply(lambda row: row['Total'] / row['Population'] if row['Population'] > 0 else np.nan, axis=1)
    merged_data['travels_per_1000_people'] = merged_data['travels_per_capita'] * 1000
    # Save to file
    merged_data.to_csv('result/merged_viagens_indicators.csv', index=False)
    print("Travels per capita and travels per 1000 people columns added and saved to 'merged_viagens_indicators.csv'.")
    return merged_data

# Show Data Profiling Report (Simplificada)
def show_data_profiling(merged_data):
    print("Detailed data profiling report")
    print("------------------------------")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    # Generate a detailed profiling report and show on screen
    profiling_report = ""
    profiling_report += "Estrutura dos dados:\n"
    buffer = io.StringIO()
    merged_data.info(buf=buffer)
    profiling_report += buffer.getvalue() + "\n\n"
    profiling_report += "Primeiras linhas dos dados:\n"
    profiling_report += str(merged_data.head()) + "\n\n"
    profiling_report += "Valores faltantes em cada coluna:\n"
    profiling_report += str(merged_data.isnull().sum()) + "\n\n"
    profiling_report += "Descrição estatística dos dados:\n"
    profiling_report += str(merged_data.describe(include='all')) + "\n\n"
    print(profiling_report)
    # Save the report to a text file
    filename = 'result/profiling_report.txt'
    with open(filename, "w") as file:
        file.write(profiling_report)
    print(f"Data profiling report saved to '{filename}'.")

# Display correlation metrics and save to CSV
def display_and_save_metrics(merged_data):
    regions = merged_data['Região'].unique()
    table_summary = []
    for region in regions:
        data_region = merged_data[merged_data['Região'] == region]
        for year in data_region['Ano'].unique():
            data_year = data_region[data_region['Ano'] == year]
            if data_year['Population'].sum() == 0:
                continue
            travel_per_1000 = (data_year['Total'].sum() / data_year['Population'].sum()) * 1000
            gni_per_capita = data_year['GNI (USD)'].sum() / data_year['Population'].sum()
            correlation = data_year['GNI (USD)'].corr(data_year['Total']) if not data_year.empty else None
            table_summary.append([year, region, round(travel_per_1000,2), int(gni_per_capita), round(correlation,2)])
    summary_df = pd.DataFrame(table_summary, columns=['Year', 'Region', 'Travel/1000', 'GNI per Capita', 'Correlation'])
    print("Correlation: Total Travel x GNI")
    print("-------------------------------")
    print(summary_df)
    filename = 'result/travel_x_GNI_correlation.csv'
    summary_df.to_csv(filename, index=False)
    print(f"Summary table saved to '{filename}'.")
    return summary_df

# Main script
def main():
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('result'):
        os.makedirs('result')
    viagens, indicators = load_csv_files()
    country_match_df = create_or_load_country_match(viagens, indicators)
    merged_data = merge_data(viagens, indicators, country_match_df)
    show_data_profiling(merged_data)
    summary_df = display_and_save_metrics(merged_data)
    print("###                Criando gráficos                   ###")
    print("###                                                   ###")
    print("### Caso algum gráfico não abra, aperte F5 no browser ###")
    p.correlation_matrix(merged_data)
    p.radar(merged_data)
    p.bubble(merged_data)
    p.boxplot_h(merged_data)
    p.boxplot_v(merged_data)
    p.worldmap_bubble(merged_data)
    p.stack_percent(merged_data)
    input("###   Executado com Sucesso. Tecle algo para fechar   ###")

if __name__ == "__main__":
    main()
