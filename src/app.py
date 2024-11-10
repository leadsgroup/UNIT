
# import dash 
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
# from dash_bootstrap_templates                # import load_figure_template
import pandas as pd  
import os



from Demographic_Maps    import * 


from Noise_Maps import generate_noise_map
from Noise_Maps import knobs_and_buttons

from CensusStatPlots import piecharts
from CensusStatPlots import knobs_and_buttons_pc



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
    
    # Section for Noise Data Controls and Graph
    html.Div([
        # Controls for Noise Selection
        html.Div([
            html.H3('Noise Analysis'),
            
            # Checklist for Vertiports and Noise Hemispheres
            knobs_and_buttons.vertiports_checklist(),
        
            # Dropdown for EVTOL Type Selection
            html.Label('EVTOL Type'),
            knobs_and_buttons.evtol_dropdown(),
            
            # Dropdown for Noise Type Selection
            html.Label('Noise Type'),
            knobs_and_buttons.noise_type_dropdown(),
            
            # Slider for Noise Level Per Tract
            html.Label('Noise Level Per Tract'),
            knobs_and_buttons.noise_slider(),
        ], style={'width': '30%'}),  
        
        # Graph for Noise Map
        html.Div([
            dcc.Graph(id='noise_map')
        ], style={'width': '70%', 'border-style': 'solid'}), 
        
    ], style={'display': 'flex', 'align-items': 'center', 'width': '80%','margin-top': '4%','margin-bottom': '8%'}),

    # Section for Pie Chart Controls and Graphs
    html.Div([
        html.H3('Pie Charts'),
        
        # Controls for Pie Charts (e.g., a test button or additional controls)
        knobs_and_buttons_pc.noise_type(),
        knobs_and_buttons_pc.noise_slider(),

        
        # Pie Charts Displayed Inline
        html.Div([
            dcc.Graph(id='pie_charts1', style={'display': 'inline-block', 'width': '45%'}),
            dcc.Graph(id='pie_charts2', style={'display': 'inline-block', 'width': '45%'}),
        ]),
        
    ], style={'width': '70%'}), 
    
], style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center'})


@callback(
    Output("noise_map", "figure"),
    Input("noise_level_slider", "value"),
    Input("noise_type_dropdown", "value")
)
def update_noise_map(noise_level_slider,noise_type_dropdown):
    fig = generate_noise_map.generate_noise_map(Noise_Data[0], noise_level_slider, noise_type_dropdown)
    return fig

@callback(
    Output("pie_charts1", "figure"),
    Output("pie_charts2", "figure"),
    Input("noise_type_dropdown_pc","value"),
    Input("noise_level_pc","value")
)
def update_pie_chart(noise_type_dropdown_pc,noise_level_pc):
    fig1,fig2 = piecharts.generate_pie_chart(Noise_Data[0], noise_level_pc, noise_type_dropdown_pc)
    return fig1,fig2

if __name__ == '__main__':
    app.run_server(debug=True)
