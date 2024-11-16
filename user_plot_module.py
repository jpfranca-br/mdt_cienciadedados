import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import os
import webbrowser

labels={'Região': 'Region',
    'Total': 'Visitors',
    'País': 'Country of Origin',
    'Região': 'Region of Origin',
    'Ano': 'Year',
    'Per Capita GNI': 'GNI per Capita (USD)',
    'Population': 'Population',
    'Marítima_pct': 'Marítima %',
    'Aérea_pct': 'Aérea_ %'
}

def save_plot(filename, fig, show):
    # Save the plot to PNG and HTML
    html_path = f"images/{filename}.html"
    fig.write_image(f"images/{filename}.png", width=1280, height=720)
    fig.write_html(html_path)
    print(f"   {filename}")
    
    # Open the HTML file in the browser if 'show' is True
    if show:
        try:
            webbrowser.open(f"file://{os.path.abspath(html_path)}", new=2)  # new=2 opens in a new tab, if possible
        except Exception as e:
            print(f"Error opening plot '{filename}': {e}")

def stack_percent(merged_data, show):
    global labels
    summarized_data = merged_data.groupby(['Ano', 'Região'])[['Marítima', 'Aérea']].sum().reset_index()
    # Create synthetic region "Todas"
    total_data = summarized_data.groupby('Ano')[['Marítima', 'Aérea']].sum().reset_index()
    total_data['Região'] = 'Todas'
    # Concatenate with summarized data
    summarized_data = pd.concat([summarized_data, total_data], ignore_index=True)
    # Calculate percentage by year and region using transform
    summarized_data['Total'] = summarized_data[['Marítima', 'Aérea']].sum(axis=1)
    summarized_data['Marítima_pct'] = summarized_data['Marítima'] / summarized_data['Total'] * 100
    summarized_data['Aérea_pct'] = summarized_data['Aérea'] / summarized_data['Total'] * 100
    # Melt data for easy plotting
    melted_data = summarized_data.melt(
        id_vars=['Ano', 'Região'],
        value_vars=['Marítima_pct', 'Aérea_pct'],
        var_name='Transport Type',
        value_name='Percentage'
    )
    # Add absolute values for hover information
    melted_data['Absolute'] = melted_data.apply(lambda row: summarized_data.loc[(summarized_data['Ano'] == row['Ano']) & (summarized_data['Região'] == row['Região']), row['Transport Type'].replace('_pct', '')].values[0], axis=1)
    # Create stacked bar chart
    fig = px.bar(
        melted_data,
        x='Ano',
        y='Percentage',
        color='Transport Type',
        animation_frame='Região',
        title='Maritime and Air Transportation Percentage by Year - Animated by Region of Origin',
        hover_name='Região',
        hover_data={'Percentage': ':.2f', 'Ano': True, 'Absolute': ':.2f'},
        labels = labels
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Visitors (%)',
        legend_title='Transport Type',
        barmode='stack'
    )
    save_plot("correlation_matrix",fig,show)
    
def correlation_matrix(merged_data, show):
    # Select only numeric columns and exclude specified columns
    numeric_data = merged_data.select_dtypes(include='number').drop(columns=['CountryID', 'travels_per_capita', 'travels_per_1000_people', 'lat', 'lon'], errors='ignore')
    # Calculate correlation matrix for each year
    if 'Ano' in merged_data.columns:
        # Create a list to hold correlation matrices for each year
        correlation_matrices = []
        for year in merged_data['Ano'].unique():
            yearly_data = numeric_data[merged_data['Ano'] == year].drop(columns=['Ano'], errors='ignore')
            correlation_matrix = yearly_data.corr().reset_index().melt(id_vars='index', var_name='Variable Y', value_name='Correlation').rename(columns={'index': 'Variable X'})
            correlation_matrix['Ano'] = year
            correlation_matrices.append(correlation_matrix)
        # Concatenate all yearly correlation matrices
        correlation_matrices = pd.concat(correlation_matrices, ignore_index=True)
        # Create heatmap with animation
        fig = px.density_heatmap(
            correlation_matrices,
            x='Variable X',
            y='Variable Y',
            z='Correlation',
            animation_frame='Ano',
            color_continuous_scale='portland_r',
            color_continuous_midpoint=0,
            title='Correlation Matrix Heatmap for All Numeric Variables - Yearly Animation'
        )
        fig.update_layout(
            #xaxis_title='Variables',
            #yaxis_title='Variables',
            yaxis=dict(autorange='reversed'),
            coloraxis_colorbar=dict(title='Correlation')
        )
        save_plot("correlation_matrix",fig,show)

def radar(merged_data, show):
    global labels
    indicators = ['Population', 'GNI (USD)', 'Total']
    sum_values = merged_data.groupby(['Ano', 'Região'])[indicators].sum().reset_index()
    categories = ['Population', 'GNI (USD)', 'Total Visitors']
    # Normalize the data using MinMaxScaler
    scaler = MinMaxScaler()
    normalized_values = sum_values.copy()
    normalized_values[indicators] = scaler.fit_transform(sum_values[indicators])
    radar_data = normalized_values.rename(columns={'Total': 'Total visitors'})
    radar_data = radar_data.rename(columns={'GNI (USD)': 'GNI (USD)', 'Total': 'Total visitors', 'Population': 'Population'})
    radar_data = radar_data.melt(id_vars=['Região', 'Ano'], var_name='Indicator', value_name='Value')
    radar_data = radar_data.merge(sum_values, on=['Região', 'Ano'])
    fig = px.line_polar(
        radar_data,
        r='Value',
        theta='Indicator',
        color='Região',
        line_close=True,
        animation_frame='Ano',
        labels=labels,
        title='Radar - GNI per capita, Total visitors, and Population by Region of Origin - Yearly Animation',
        hover_name='Região',
        hover_data=['GNI (USD)','Population','Total']
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        legend_title='Region of Origin'
    )
    save_plot("radar",fig,show)
  
def bubble(merged_data, show):
    global labels
    fig = px.scatter(
        merged_data.fillna({"Population": 1}),
        title='Bubble plot - Visitors, GNI per Capita, Population, Region - Yearly Animation',
        y="Per capita GNI",
        x="Total",
        animation_frame="Ano",
        animation_group="País",
        color="Região",
        hover_name="País",
        log_x=True,
        log_y=True,
        size = "Population",
        size_max=100,
        range_y=[200,2e5],
        range_x=[50,5e5],
        labels=labels
    )
    fig.update_layout(
        xaxis_title='Visitors',
        yaxis_title='GNI per Capita (USD)',
        legend_title='Region of Origin'
    )
    save_plot("bubble",fig,show)
    
def boxplot_h(merged_data, show):
    global labels
    fig = px.box(
        merged_data,
        x='Região',
        y='Total',
        color='Região',
        animation_frame='Ano',
        points='outliers',
        title='Boxplot - Visitors by Region and Country of Origin - Yearly Animation',
        labels=labels,
        hover_name='País',
        hover_data=['Total']
    )
    fig.update_layout(
        xaxis_title='Region of Origin',
        yaxis_title='Visitors',
        legend_title='Region of Origin',
        #yaxis=dict(range=[0, merged_data['Total'].max() * 1.0])
        yaxis=dict(range=[0, 250000])
    )
    save_plot("boxplot_horizontal",fig,show)

def boxplot_v(merged_data, show):
    global labels
    fig = px.box(
        merged_data,
        y='Região',
        x='Total',
        color='Região',
        animation_frame='Ano',
        points='outliers',
        title='Boxplot - Visitors by Region and Country of Origin - Yearly Animation',
        labels=labels,
        hover_name='País',
        hover_data=['Total']
    )
    fig.update_layout(
        yaxis_title='Region of Origin',
        xaxis_title='Visitors',
        legend_title='Region of Origin',
        #xaxis=dict(range=[0, merged_data['Total'].max() * 1.0])
        xaxis=dict(range=[0, 250000])
    )
    save_plot("boxplot_vertical",fig,show)

def worldmap_bubble(merged_data, show):
    global labels
    fig = px.scatter_geo(
        merged_data,
        locations='País',
        locationmode='country names',
        size='Total',
        animation_frame='Ano',
        title='Worldmap Bubble - Visitors by Country of Origin - Yearly Animation',
        labels=labels,
        hover_name='País',
        color='Região',
        size_max=60
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        coloraxis_colorbar=dict(title='Total Visitors')
    )
    save_plot("worldmap_bubble",fig,show)
