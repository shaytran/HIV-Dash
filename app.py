import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table, State, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import json

df_aggregated = pd.read_csv("data/processed/dash_clean.csv", index_col=0, low_memory=False)

app = Dash(__name__, title="HIV Dash", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

## Add dataset and github icon
def modal_data_source():
    return dmc.Modal(
            id='modal-data-source',
            size='55%',
            styles={
                'modal': {
                    'background-color': '#f2f2f2',
                }
            },
            children=[
                dcc.Markdown(
                    [
                        """
                        
                        # About the Dataset
                        
                        HIV (Human Immunodeficiency Virus) is a well-known virus that attacks the immune system of infected individuals. 
                        HIV gained immense awareness in the early 1980s, particularly in the USA, and it is responsible for AIDS (Acquired Immunodeficiency Syndrome), 
                        which is a stage of HIV infection where the immune system is severely damaged. As of 2022, 
                        there were approximately 39 million people globally that are living with HIV/AIDS, which has no known cure so far. 
                        HIV/AIDS remains a global public health issue, with ongoing efforts to increase access to prevention, treatment, and care.

                        This dataset contains 12 indicators. These indicators can be categorized into two main groups:

                        1. General rates (ie. rate of annual AIDS-related deaths, incidence rate, mother-to-child transmission rate)
                        2. Statistics on pregnant women and children (ie. number of children receiving ART, percent of pregnant women living with HIV within 2 months of birth, 
                           estimated children who have lost one or both parents due to AIDS)

                        ## Source Information
                        
                        - **Title:** "Key HIV epidemiology indicators for children and adolescents aged 0-19, 2000-2022"
                        - **Published Online:** data.unicef.org
                        - **Retrieved From:** [UNICEF](https://data.unicef.org/resources/dataset/hiv-aids-statistical-tables/)
                        - **Temporal Coverage:** From 01/01/2000 to 12/31/2022
                        - **Geospatial Coverage:** Worldwide
                        
                        ## Collection Methodology
                        
                        The data was collected by visiting the publisher.
                        
                        """
                    ],
                )
            ]
        )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("HIV Indicator Dashboard", style={"color": "burgundy"}),
                dmc.Grid(
                    [
                        modal_data_source(),
                        dmc.Col(
                            dmc.Group(
                                [
                                    dmc.ActionIcon(
                                        [DashIconify(icon='bx:data', color='#C8C8C8', width=25)],
                                        variant='transparent',
                                        id='about-data-source'
                                    ),
                                    dmc.Anchor(
                                        [DashIconify(icon='uil:github', color='#8d8d8d', width=30)],
                                        href='https://github.com/shaytran/HIV-Dash'
                                    )
                                ],
                                spacing='xl',
                                position='center'
                            ),
                        )
                    ],
                    justify="center"
                )
            ], style={"textAlign": "center"}),
            width={"size": 12, "offset": 0}
        )
    ], align="center", style={"margin-bottom": "20px"}),
    html.Img(src="https://cdn.storymd.com/optimized/RqVLDEsxom/thumbnail.gif", style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "10%"}),
    html.P("HIV (Human Immunodeficiency Virus) attacks the immune system and can lead to AIDS (Acquired Immunodeficiency Syndrome), a condition where the immune system is severely damaged. First identified in the early 1980s in the USA, HIV/AIDS has since become a global public health issue, with approximately 39 million people living with the virus worldwide as of 2022. Despite significant advancements, there is no cure for HIV/AIDS, highlighting the importance of continued efforts in prevention, treatment, and care.", style={"textAlign": "center", "color": "burgundy"}),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Indicator Trend', children=[
            html.H2('HIV Indicator Trends by Country and Year', style={"textAlign": "center"}),
            html.P('Select an HIV indicator and up to 4 countries to compare their trends over time. You can toggle the year range using the sliding bar.', style={"textAlign": "center"}),
            html.Div(id='missing-data-warning', style={'textAlign': 'center', 'color': 'red'}),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='indicator-dropdown',
                        value=df_aggregated.columns[3],  # Default value is the first indicator column
                        options=[{'label': col, 'value': col} for col in df_aggregated.columns[3:]], 
                        placeholder='Choose 1 indicator...'
                    ),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in df_aggregated['Geographic area'].unique()],
                        placeholder='Choose up to 4 countries...',
                        multi=True
                    ),
                    html.Div([
                        dcc.RangeSlider(
                            id='year-slider',
                            min=df_aggregated['Time period'].min(),
                            max=df_aggregated['Time period'].max(),
                            marks={str(year): str(year) for year in range(df_aggregated['Time period'].min(), df_aggregated['Time period'].max() + 1)},
                            step=1,
                            value=[df_aggregated['Time period'].min(), df_aggregated['Time period'].max()]
                        )
                    ], style={'marginTop': 20})
                ])
            ]),
            html.Div(id='trend-chart')
        ]),
        ### Second tab
        dcc.Tab([
            html.H2("Global Spread of HIV Indicator", style={"textAlign": "center"}),
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
                dbc.Col(dcc.Graph(id='world-map'))
            ])   
        ], label='Indicator Map'),
        ### Third tab
        dbc.Tab([
            html.H2('Indicator Summary Statistics', style={"textAlign": "center"}),
            html.Div(id='summary-stats-message', style={'color': 'red', 'marginBottom': '20px'}),  # Message display component
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='indicator-stats-dropdown',
                        value=df_aggregated.columns[3],  # Default value is the first indicator column
                        options=[{'label': col, 'value': col} for col in df_aggregated.columns[3:]], 
                        placeholder='Choose 1 indicator...'
                    ),
                    dcc.Dropdown(
                        id='country-stats-dropdown',
                        options=[{'label': country, 'value': country} for country in df_aggregated['Geographic area'].unique()],
                        placeholder='Choose up to 10 countries...',
                        multi=True  # Allow multiple selections, but limit to 10 for the stats comparison
                    ),
                ]),
            ]),
            # Moving the DataTable to be the first element inside the tab, so it grows above the slider
            dbc.Row([
                dash_table.DataTable(id='summary-stats-table')
            ]),
            # Adding the year slider below the DataTable
            dbc.Row([
                dcc.RangeSlider(
                    id='year-stats-slider',
                    min=df_aggregated['Time period'].min(),
                    max=df_aggregated['Time period'].max(),
                    value=[df_aggregated['Time period'].min(), df_aggregated['Time period'].max()],
                    marks={str(year): str(year) for year in range(df_aggregated['Time period'].min(), df_aggregated['Time period'].max() + 1)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'marginTop': '20px', 'marginBottom': '20px'}),  # Adding space above and extra space below the slider
        ], label='Indicator Summary Statistics')
    ])
], style={'backgroundColor': '#FFFFFF', "color": "#2F3C48"})

## Callback for the dataset and github icons
clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='toggle_modal_data_source'),
    Output('modal-data-source', 'opened'),
    Input('about-data-source', 'n_clicks'),
    State('modal-data-source', 'opened'),
    prevent_initial_call=True
)

# Callback for updating the chart based on selections
@app.callback(
    [Output('trend-chart', 'children'), Output('missing-data-warning', 'children')],
    [Input('indicator-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_chart(selected_indicator, selected_countries, selected_years):
    if selected_countries is None or selected_indicator is None or len(selected_countries) > 4:
        return [html.Div('Please select an indicator and up to 4 countries.')], None

    chart_df = df_aggregated[(df_aggregated['Time period'].between(selected_years[0], selected_years[1])) & (df_aggregated['Geographic area'].isin(selected_countries))]

    if chart_df.empty:
        return [html.Div()], 'No data available for the selected criteria.'

    missing_countries = [country for country in selected_countries if country not in chart_df['Geographic area'].unique()]
    warning_msg = None
    if missing_countries:
        warning_msg = f"Missing data for countries: {', '.join(missing_countries)}"

    # Creating a line chart using Plotly
    fig = px.line(chart_df, x="Time period", y=selected_indicator, color='Geographic area', title=f"Trend of {selected_indicator}", labels={"Time period": "Year"})
    
    # Update the layout to remove y-axis title
    fig.update_layout(
        yaxis_title="",
        margin=dict(l=100, r=100, t=100, b=100),  
        width=1200,  
        height=600,  
        transition_duration=500
    )


    return [dcc.Graph(figure=fig)], warning_msg

# Callback for updating the map based on dropdown and slider values
@app.callback(
    Output('world-map', 'figure'),
    Input('indicator-map-dropdown', 'value')
)

def update_figures(selected_indicator):
    fig_map = px.scatter_geo(
        df_aggregated,
        locations='Geographic area',
        locationmode='country names',
        color=selected_indicator,
        color_continuous_scale=px.colors.cyclical.IceFire,
        hover_name='Geographic area',
        # Limit the information to display on the hover box
        hover_data={'Time period':False,
                    'Geographic area':False,
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
        labels={'size': 'Value',
                'Estimated rate of annual AIDS-related deaths (per 100,000 population)': "Estimated rate",
                'Estimated incidence rate (new HIV infection per 1,000 uninfected population)': "Estimated rate",
                'Reported number of children (aged 0-14 years) receiving antiretroviral treatment (ART)': "Reported number",
                'Per cent of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth': "Reported rate",
                'Reported number of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth': "Reported number",
                'Estimated number of children (aged 0-17 years) who have lost one or both parents due to all causes': "Estimated number",
                'Estimated number of children (aged 0-17 years) who have lost one or both parents due to AIDS': "Estimated number",
                'Per cent of pregnant women living with HIV receiving lifelong ART': "Reported rate",
                'Reported number of pregnant women living with HIV receiving lifelong antiretroviral treatment (ART)': "Reported number",
                'Per cent of pregnant women living with HIV receiving effective ARVs for PMTCT (excludes single-dose nevirapine)': "Reported rate",
                'Reported number of pregnant woment living with HIV receiving anitretroviral treatments (ARVs) for prevention of mother to child transmission programmes (PMTCT)': "Reported number",
                'Mother-to-child HIV transmission rate': "Reported rate"
                },
        animation_frame='Time period',
        animation_group='Geographic area',
        size=df_aggregated[selected_indicator].fillna(0),
        size_max=20,
        projection='natural earth',
    )
    # Remove the legend since some of the column names are too long and will squeeze the size of the map
    # fig.update(layout_coloraxis_showscale=False)
    fig_map.update_geos(
        showcountries=True, countrycolor='whitesmoke',
        showland=True, landcolor='dimgrey',
        showocean=True, oceancolor="Black"
    )
    fig_map.update_layout(
        title=f"{selected_indicator}",
        title_x=0.5,
        title_font_size=14,
        height=650,
        width=1300
    )
    return fig_map

# Callback for updating the summary statistics table
@app.callback(
    Output('summary-stats-table', 'data'),
    Output('summary-stats-table', 'columns'),
    Output('summary-stats-message', 'children'),  # Assuming you add this component for messages
    [Input('indicator-stats-dropdown', 'value'),
     Input('country-stats-dropdown', 'value'),
     Input('year-stats-slider', 'value')]
)
def update_summary_statistics(selected_indicator, selected_countries, selected_years):
    print("Callback Triggered")  # For debugging

    if not selected_indicator:
        return [], [], 'Please select an indicator.'
    
    if not selected_countries:
        return [], [], ''
    
    if len(selected_countries) > 10:
        # If more than 10 countries are selected, return a message asking to reduce the selection
        return [], [], 'Please select only up to 10 countries.'

    # Filter based on the selected years and countries
    stats_df = df_aggregated[df_aggregated['Time period'].between(*selected_years)]
    stats_df = stats_df[stats_df['Geographic area'].isin(selected_countries)]

    # Compute summary statistics
    summary = stats_df.groupby('Geographic area')[selected_indicator].agg(['mean', 'min', 'max', 'count']).reset_index()

    # Check for rows where Non-null Count is 0 and set Mean, Min, Max to 'NULL'
    for i in summary.index:
        if summary.at[i, 'count'] == 0:
            summary.at[i, 'mean'] = 'NULL'
            summary.at[i, 'min'] = 'NULL'
            summary.at[i, 'max'] = 'NULL'

    # Rename columns for better readability in the DataTable
    summary.columns = ['Geographic area', 'Mean', 'Min', 'Max', 'Non-null Count']

    # Convert to records format for DataTable
    data = summary.to_dict('records')
    columns = [{"name": i, "id": i} for i in summary.columns]

    # No error message if criteria are met
    return data, columns, None

if __name__ == '__main__':
    app.run_server()