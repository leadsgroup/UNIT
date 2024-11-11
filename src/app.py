# import necessary libraries
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os

from Demographic_Maps import *
from Noise_Maps import generate_noise_map, knobs_and_buttons
from CensusStatPlots import generate_pie_chart, knobs_and_buttons_pc
from Dashboard_Elements import generate_dash_elements

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------------------------------------------------------------------- 
# Define the separator for file paths
separator = os.path.sep

# Update the filenames for raw census data (race and income) in the Processed_Data directory
census_race_filename = '..' + separator + 'Processed_Data' + separator + 'RawCensusDataRace.xlsx'
census_income_filename = '..' + separator + 'Processed_Data' + separator + 'RawCensusDataIncome.xlsx'
noise_filename = '..' + separator + 'Processed_Data' + separator + 'TR_1000ft_LA_10min_Allper_tract.xlsx'

# Load the Excel files for race and income
Census_Race_Data = pd.read_excel(census_race_filename, sheet_name=None)  # None will load all sheets
Census_Income_Data = pd.read_excel(census_income_filename, sheet_name=None)  # None will load all sheets
Noise_TR_Data = pd.read_excel(noise_filename)  # None will load all sheets

# Store census data
Census_Data = [Census_Income_Data, Census_Race_Data]
# Store aircraft noise data
Noise_Data = [Noise_TR_Data]

# Initialize the Dash app with Bootstrap themes
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # Try using CYBORG theme for dark mode
app.title = "Urban Noise Impact Tool"

# App layout
app.layout = dbc.Container([
    # Title and Theme Switch
    dbc.Row([
        dbc.Col(html.H2("Urban Noise Impact Tool", id="app-title", className="text-center my-4"),
                style={'backgroundColor': '#007bff', 'padding': '2%'})
    ], justify="center"),

    dbc.Row([generate_dash_elements.color_switch()], justify="center"),

    # Main content sections
    dbc.Row([
        # Noise Controls and Map
        dbc.Col([
            html.Div([
                html.H3('Noise Analysis', className="bg-primary text-light"),
                knobs_and_buttons.vertiports_checklist(),
                html.Label('EVTOL Type', id="evtol-label"),
                knobs_and_buttons.evtol_dropdown(),
                html.Label('Noise Type', id="noise-type-label"),
                knobs_and_buttons.noise_type_dropdown(),
                html.Label('Noise Level Per Tract', id="noise-level-label"),
                knobs_and_buttons.noise_slider(),
            ], style={'padding': '10px', 'border': '1px solid #555'})
        ], width=4, id="controls-section", style={'padding': '20px', 'border-radius': '8px'}),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Noise Map", className="bg-primary text-light"),
                dbc.CardBody([dcc.Graph(id='noise_map')])
            ], style={'width': '90%', 'margin': '0 auto'})
        ], width=8, id="noise-section"),
    ], className="my-4 justify-content-center"),

    # Pie Chart Controls and Graphs
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Pie Charts", className="bg-primary text-light"),
                dbc.CardBody([
                    knobs_and_buttons_pc.noise_type(),
                    knobs_and_buttons_pc.noise_slider(),
                    html.Div([
                        dcc.Graph(id='pie_charts1', style={'display': 'inline-block', 'width': '45%'}),
                        dcc.Graph(id='pie_charts2', style={'display': 'inline-block', 'width': '45%'}),
                    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
                ])
            ], style={'width': '100%', 'margin': '0 auto'})
        ], width=10)
    ], className="justify-content-center", id="pie-chart-section")
], fluid=True, id="app-container", style={'maxWidth': '100%', 'margin': '0 auto'})

# Callback to update theme, background, and text colors
@callback(
    [Output("app-container", "style"),
     Output("app-title", "style"),
     Output("theme-label", "style"),
     Output("evtol-label", "style"),
     Output("noise-type-label", "style"),
     Output("noise-level-label", "style"),
     Output('controls-section', "style"),
     Output('pie-chart-section', "style")],
    [Input("theme-switch", "value")]
)
def theme_callback(selected_theme):
    return generate_dash_elements.update_theme(selected_theme)

@callback(
    Output("noise_map", "figure"),
    Input("noise_level_slider", "value"),
    Input("noise_type_dropdown", "value")
)
def update_noise_map(noise_level_slider, noise_type_dropdown):
    fig = generate_noise_map.generate_noise_map(Noise_Data[0], noise_level_slider, noise_type_dropdown)
    return fig

@callback(
    Output("pie_charts1", "figure"),
    Output("pie_charts2", "figure"),
    Input("noise_type_dropdown_pc", "value"),
    Input("noise_level_pc", "value")
)
def update_pie_chart(noise_type_dropdown_pc,noise_level_pc):
    fig1,fig2 = generate_pie_chart.generate_pie_chart(Noise_Data[0], noise_level_pc, noise_type_dropdown_pc)
    return fig1,fig2

if __name__ == '__main__':
    app.run_server(debug=True)
