import user_plot_module as p
import pandas as pd
import os
import unidecode
import numpy as np
import io
import keyboard

def main():
    show_reports = False  # Show reports on screen?
    show_plots = True  # Show plots on screen?

    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('result'):
        os.makedirs('result')

    print(f"Showing reports on screen: {show_reports}")
    print(f"Showing plots on screen: {show_plots}")

    viagens, indicators = load_csv_files()
    country_match_df = create_or_load_country_match(viagens, indicators)

    if country_match_df is not None and not country_match_df.empty:
        merged_data = merge_data(viagens, indicators, country_match_df)
        data_profiling(merged_data, show_reports)
        summary_df = correlation(merged_data, show_reports)
        print("Building plots. It will take a few seconds...")
        plot_names = [
            'correlation_matrix',
            'radar',
            'bubble',
            #'boxplot_h',
            'boxplot_v',
            'worldmap_bubble',
            'stack_percent'
        ]
        plot(merged_data, show_plots, 'mt', plot_names) #mp for multiprocessor, #mt for multithread, whatever else for single thread
        print("Plots saved.")

    print("All done! Press any key to close.")
    keyboard.read_event()

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
    print("Building or loading country match table...")
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
        print("ERROR: File 'data/country_match.csv' not found.")
        print("       Standard table generated and saved to 'result/country_match.csv'.")
        print("       Please make the appropriate country matches and save csv to data/ folder.")
        return None
    else:
        country_match_df = pd.read_csv('data/country_match.csv')
        print("Loaded existing country match table from 'country_match.csv'.")
    return country_match_df

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
    unique_countries_matched = merged_data['País'].nunique()
    print(f"Number of countries matched: {unique_countries_matched}")
    merged_data = merged_data.merge(indicators, how='left', left_on=['indicators_country', 'Ano'], right_on=['Country', 'Year'])
    # Calculate travels per capita / per 1000 people
    merged_data['travels_per_capita'] = merged_data.apply(lambda row: row['Total'] / row['Population'] if row['Population'] > 0 else np.nan, axis=1)
    merged_data['travels_per_1000_people'] = merged_data['travels_per_capita'] * 1000
    # Save to file
    merged_data.to_csv('result/merged_viagens_indicators.csv', index=False)
    print("Data merged and enriched.")
    print("Full table saved to 'result/merged_viagens_indicators.csv'.")
    return merged_data

# Data Profiling Report
def data_profiling(merged_data, show):
    print("Building detailed data profiling report...")
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
    if (show):
        print(profiling_report)
    # Save the report to a text file
    filename = 'result/profiling_report.txt'
    with open(filename, "w") as file:
        file.write(profiling_report)
    print(f"Data profiling report saved to '{filename}'.")

# Generate correlation and save to CSV
def correlation(merged_data, show):
    print("Building correlation report...")
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
    if (show):
        print("Correlation: Total Travel x GNI")
        print("-------------------------------")
        print(summary_df)
    filename = 'result/correlation.csv'
    summary_df.to_csv(filename, index=False)
    print(f"Correlation report saved to '{filename}'.")
    return summary_df

# Plot function
def plot(merged_data, show_plots, multi, plot_names):
    multi = multi.lower()
    plot_functions = [
        (getattr(p, name), merged_data, show_plots)
        for name in plot_names if hasattr(p, name)
    ]
    if not plot_functions:
        print("No valid plot names provided. Exiting plot function.")
        return
    if multi == 'mt':
        import concurrent.futures
        #import multiprocessing
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(func, *args) for func, *args in plot_functions]
            concurrent.futures.wait(futures)
    elif multi == 'mp':
        import concurrent.futures
        #import multiprocessing
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(func, *args) for func, *args in plot_functions]
            concurrent.futures.wait(futures)
    else:
        for func, *args in plot_functions:
            func(*args)

if __name__ == "__main__":
    main()
