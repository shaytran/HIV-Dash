import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import altair as alt

df_aggregated = pd.read_csv("data/processed/dash_clean.csv", index_col=0, low_memory=False)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("HIV Indicator Dashboard", style={"textAlign": "center"}),
    dcc.Tabs(id='tabs', children=[
        ### First tab
        dcc.Tab([ 
            html.H2('HIV Indicator Trends by Country and Year'),
            html.P('Select an indicator and up to 4 countries to compare their trends over time.'),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='indicator-dropdown',
                        value=df_aggregated.columns[3],  # Default value is the first indicator column
                        options=[{'label': col, 'value': col} for col in df_aggregated.columns[3:]], 
                        placeholder='Choose 1 indicator...'),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in df_aggregated['Geographic area'].unique()],
                        placeholder='Choose up to 4 countries...',
                        multi=True)  # Allow multiple selections
                ]),
            ]),
            dbc.Row([
                html.Iframe(id='trend-chart', style={'border-width': '0', 'width': '100%', 'height': '400px'}),
                dcc.RangeSlider(
                        id='year-slider',
                        min=df_aggregated['Time period'].min(),
                        max=df_aggregated['Time period'].max(),
                        marks={str(year): str(year) for year in range(df_aggregated['Time period'].min(), df_aggregated['Time period'].max() + 1)},
                        step=1,
                        value=[df_aggregated['Time period'].min(), df_aggregated['Time period'].max()]
                )
            ])
        ], label='Indicator Trend'),
        ### Second tab
        dcc.Tab([
            html.H2("HIV Indicator map"),
                dbc.Row([
                # Dropdown for selecting indicator
                    dcc.Dropdown(
                        id='indicator-map-dropdown',
                        # Limiting the usage of indicator columns to avoid errors since some of them are in non-numeric type at the moment
                        options=[{'label': col, 'value': col} for col in df_aggregated.columns[3:]],
                        value=df_aggregated.columns[3],  # Initial indicator
                        multi=False,
                )]),
                dbc.Row([
                    # Map
                    dcc.Graph(id='world-map'),
                    # Slider for selecting year
                    dcc.Slider(
                        id='year-map-slider',
                        min=df_aggregated['Time period'].min(),
                        max=df_aggregated['Time period'].max(),
                        value=df_aggregated['Time period'].max(),  # Set default displayed year as 2022
                        marks={str(year): str(year) for year in df_aggregated['Time period'].unique()},
                        step=1,
                )])],
            label='Indicator Map'    
        ),
        ### Third tab
        dcc.Tab([
            html.H2('Indicator Summary Statistics'),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='indicator-stats-dropdown',
                        value=df_aggregated.columns[4],  # Default value is the first indicator column
                        options=[{'label': col, 'value': col} for col in df_aggregated.columns[4:]], 
                        placeholder='Choose 1 indicator...'
                    ),
                    dcc.Dropdown(
                        id='country-stats-dropdown',
                        options=[{'label': country, 'value': country} for country in df_aggregated['Geographic area'].unique()],
                        placeholder='Choose up to 10 countries...',
                        multi=True  # Allow multiple selections, but limit to 2 for the stats comparison
                    )
                ]),
                dcc.RangeSlider(
                    id='year-stats-slider',
                    min=df_aggregated['Time period'].min(),
                    max=df_aggregated['Time period'].max(),
                    value=[df_aggregated['Time period'].min(), df_aggregated['Time period'].max()],
                    marks={str(year): str(year) for year in range(df_aggregated['Time period'].min(), df_aggregated['Time period'].max() + 1)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ]),
            dbc.Row([
                dash_table.DataTable(id='summary-stats-table')
            ])
        ], label='Indicator Summary Statistics')
    ])    
])

# Callback for updating the chart based on selections
@app.callback(
    Output('trend-chart', 'srcDoc'),
    [Input('indicator-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_chart(selected_indicator, selected_countries, selected_years):
    if selected_countries is None or selected_indicator is None or len(selected_countries) > 4:
        return 'Please select an indicator and up to 4 countries.'

    # Filter based on the selected years and countries
    chart_df = df_aggregated[df_aggregated['Time period'].between(*selected_years)]
    chart_df = chart_df[chart_df['Geographic area'].isin(selected_countries)]
    
    # Create the Altair chart
    base = alt.Chart(chart_df).encode(
        x=alt.X('Time period:O', axis=alt.Axis(title='Year')),
        y=alt.Y(f"{selected_indicator}:Q", axis=alt.Axis(title=selected_indicator)),
        color='Geographic area:N'
    )
    
    line_chart = base.mark_line(point=True).properties(
        width=700,
        height=400
    )
    
    return line_chart.to_html()

# Callback for updating the map based on dropdown and slider values
@app.callback(
    Output('world-map', 'figure'),
    [Input('indicator-map-dropdown', 'value'),
     Input('year-map-slider', 'value')]
)
def update_map(selected_indicator, selected_year):
    filtered_data = df_aggregated[(df_aggregated['Time period'] == selected_year)]
    fig = px.scatter_geo(
        filtered_data,
        locations='Geographic area',
        locationmode='country names',
        color=selected_indicator,
        hover_name='Geographic area',
        # Limit the information to display on the hover box
        hover_data={'Geographic area':False,
                    'Estimated rate of annual AIDS-related deaths (per 100,000 population)':False,
                    'Estimated incidence rate (new HIV infection per 1,000 uninfected population)':False,
                    'Reported number of children (aged 0-14 years) receiving antiretroviral treatment (ART)':False,
                    'Per cent of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth':False,
                    'Reported number of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth':False,
                    'Estimated number of children (aged 0-17 years) who have lost one or both parents due to all causes':False,
                    'Estimated number of children (aged 0-17 years) who have lost one or both parents due to AIDS':False,
                    'Per cent of pregnant women living with HIV receiving lifelong ART':False,
                    'Reported number of pregnant women living with HIV receiving lifelong antiretroviral treatment (ART)':False,
                    'Per cent of pregnant women living with HIV receiving effective ARVs for PMTCT (excludes single-dose nevirapine)':False,
                    'Reported number of pregnant woment living with HIV receiving anitretroviral treatments (ARVs) for prevention of mother to child transmission programmes (PMTCT)':False,
                    'Mother-to-child HIV transmission rate':False},
        labels={'size': 'Value'},
        size=filtered_data[selected_indicator].fillna(0),
        size_max=20,
        projection='natural earth',
    )
    # Remove the legend since some of the column names are too long and will squeeze the size of the map
    fig.update(layout_coloraxis_showscale=False)
    fig.update_geos(
        showcountries=True, countrycolor='whitesmoke',
        showland=True, landcolor='dimgrey',
        showocean=True, oceancolor="Black"
    )
    fig.update_layout(
        title=f"{selected_indicator} in {selected_year}",
        title_x=0.5,
        title_font_size=14
    )
    return fig

# Callback for updating the summary statistics table
@app.callback(
    [Output('summary-stats-table', 'data'), Output('summary-stats-table', 'columns')],
    [Input('indicator-stats-dropdown', 'value'),
     Input('country-stats-dropdown', 'value'),
     Input('year-stats-slider', 'value')]
)
def update_summary_statistics(selected_indicator, selected_countries, selected_years):
    print("Callback Triggered")  # For debugging, check the console where you run the server

    if not selected_countries or not selected_indicator or len(selected_countries) > 10:
        return [], []

    # Filter based on the selected years and countries
    stats_df = df_aggregated[df_aggregated['Time period'].between(*selected_years)]
    stats_df = stats_df[stats_df['Geographic area'].isin(selected_countries)]

    # Compute summary statistics
    summary = stats_df.groupby('Geographic area')[selected_indicator].agg(['mean', 'min', 'max', 'count']).reset_index()

    # Rename columns for better readability in the DataTable
    summary.columns = ['Geographic area', 'Mean', 'Min', 'Max', 'Non-null Count']

    # Convert to records format for DataTable
    data = summary.to_dict('records')
    columns = [{"name": i, "id": i} for i in summary.columns]

    return data, columns

if __name__ == '__main__':
    app.run_server(debug=True)