
import dash 
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates                  import load_figure_template 
import pandas as pd  
import os
import plotly.express as px



from Demographic_Maps    import * 
from Noise_Maps import generate_noise_map
from CensusStatPlots import piecharts

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

#store census data
Census_Data = [Census_Income_Data,Census_Race_Data]
#store aircraft noise data
Noise_Data = [Noise_TR_Data]

app = Dash(__name__)

# app layout
app.layout = html.Div([

    # Map Types Section for Race
    html.Div([
        html.H3('Map Types'),
        dcc.Checklist(
            options=[{'label': 'Topography', 'value': 'Topography'}],
            value=['Topography'],
            style={'margin-bottom': '10px'}
        ),
        html.Label('Race'),
        dcc.Dropdown(
            options=[
                {'label': 'Percent Hispanic/Latino', 'value': 'Hispanic/Latino'},
                {'label': 'Percent Black/African American', 'value': 'Black/African American'},
                {'label': 'Percent White', 'value': 'White'},
            ],
            value=['Hispanic/Latino', 'Black/African American', 'White'],
            multi=True,
            style={'margin-bottom': '20px'}
        ),
        html.Label('Income'),
        dcc.Dropdown(
            options=[
                {'label': '$0 - $10,000', 'value': '0-10000'},
                {'label': '$10,000 - $20,000', 'value': '10000-20000'},
                {'label': '$20,000 - $30,000', 'value': '20000-30000'},
                {'label': '$30,000 - $40,000', 'value': '30000-40000'},
                {'label': '$40,000 - $50,000', 'value': '40000-50000'},
                {'label': '$50,000 - $60,000', 'value': '50000-60000'},
                {'label': '$60,000 - $70,000', 'value': '60000-70000'},
                {'label': '$70,000 - $80,000', 'value': '70000-80000'},
                {'label': '$80,000 - $90,000', 'value': '80000-90000'},
                {'label': '$90,000 - $100,000', 'value': '90000-100000'},
            ],
            value=[],
            multi=True,
            id="income_range",
            style={'margin-bottom': '20px'}
        ),
        html.Label('Sensitive Areas'),
        dcc.Dropdown(
            options=[{'label': 'Churches', 'value': 'Churches'},
                     {'label': 'Hospitals/Medical Centers', 'value': 'Hospitals/Medical Centers'},
                     {'label': 'Schools/Universities', 'value': 'Schools/Universities'}, ],
            value=[],
            multi=True,
            style={'margin-bottom': '20px'}
        )
    ], style={'padding': 10, 'border': '1px solid #d3d3d3', 'margin-bottom': '20px'}),  # Added margin to separate from noise section

    # Graph for Race Map
    dcc.Graph(id='income_map'),  # This is where the race map will be displayed
# Noise Data Section

# Map Types Section for Race
    html.Div([
        html.H3('piecharts'),
        
    # Graph for Race Map
    dcc.Graph(id='pie_charts') , # This is where the race map will be displayed
# Noise Data Section
html.Div([
    html.H3('Noise Data'),
    
    dcc.Checklist(
        options=[{'label': 'Vertiports', 'value': 'Vertiports'}],
        value=['Vertiports'],
        style={'margin-bottom': '10px'}
    ),
    dcc.Checklist(
        options=[{'label': 'Noise Hemispheres', 'value': 'Noise Hemispheres'}],
        value=[],
        style={'margin-bottom': '10px'}
    ),
    
    # EVTOL Type Dropdown
    html.Label('EVTOL Type'),
    dcc.Dropdown(
        options=[
            {'label': 'Stopped Rotor', 'value': 'Stopped Rotor'},
            {'label': 'Tilt Rotor', 'value': 'Tilt Rotor'},
            {'label': 'Hexacopter', 'value': 'Hexacopter'},
        ],
        value='Stopped Rotor',
        style={'margin-bottom': '20px'}
    ),

    # Noise Type Dropdown
    html.Label('Noise Type'),
    dcc.Dropdown(
        id='noise_type_dropdown',  # New dropdown for noise type
        options=[
            {'label': 'L_AeqT', 'value': 'L_AeqT'},
            {'label': 'L_AeqT_24hr', 'value': 'L_AeqT_24hr'},
            {'label': 'SEL', 'value': 'SEL'},
            {'label': 'L_dn', 'value': 'L_dn'},
            {'label': 'L_Aeq_jetliner', 'value': 'L_Aeq_jetliner'},
            {'label': 'L_Amax', 'value': 'L_Amax'}
        ],
        value='L_AeqT',  # Default selection
        style={'margin-bottom': '20px'}
    ),

    # Noise Level Slider
    html.Label('Noise Level Per Tract'),
    dcc.Slider(
        id='noise_level_slider',
        min=0,
        max=80,
        step=1,
        marks={i: f'{i} dB' for i in range(0, 81, 20)},
        value=40
    )
], style={'padding': 10, 'border': '1px solid #d3d3d3', 'margin-bottom': '20px'}),

# Graph for Noise Map
dcc.Graph(id='noise_map'),  # This is where the noise map will be displayed

], style={'display': 'flex', 'flexDirection': 'column'})

])
# @callback(
#     Output("income_map", "figure"),
#     Input("income_range", "value"), 
#     Input("color-mode-switch", "value"), 
# )
# def update_battery_comparison_figure(income_range,switch_off):     
#     fig  = generate_income_map(Census_Data,income_range,switch_off)  
#     return fig

@callback(
    Output("noise_map", "figure"),
    Input("noise_level_slider", "value"),
    Input("noise_type_dropdown", "value")
)
def update_noise_map(noise_level_slider,noise_type_dropdown):
    fig = generate_noise_map.generate_noise_map(Noise_Data[0], noise_level_slider, noise_type_dropdown)
    return fig

@callback(
    Output("pie_charts", "figure1"),
    Output("pie_charts", "figure2"),
    Output("pie_charts", "figure3")
    Input("noise_level_slider", "value")
    # Input("noise_type_dropdown", "value")
)
def update_pie_chart(noise_level_slider):
    fig1,fig2,fig3 = piecharts.generate_pie_chart()
    return fig1,fig2,fig3

if __name__ == '__main__':
    app.run_server(debug=True)
