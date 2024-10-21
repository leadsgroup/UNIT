
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Sample Data for Pie Charts
race_data = pd.DataFrame({
    'Race': ['Hispanic/Latino', 'Black/African American', 'White'],
    'Percentage': [30, 40, 30]
})

income_data = pd.DataFrame({
    'Income Range': [
        '0-30,000', '30,00-60,000', '60,00-90,000', '90,00-100,000'
    ],
    'Percentage': [30, 30, 25, 15]
})

sensitive_areas_data = pd.DataFrame({
    'Sensitive Areas': ['Churches', 'Hospitals/Medical Buildings', 'Schools/Universities'],
    'Density': [40, 35, 25]
})

# Colors for the Pie Charts (cohesive color scheme)
colors = ['#636EFA', '#EF553B', '#00CC96']

# Create Pie Charts with Hover and Uniform Sizes
race_pie = px.pie(race_data, names='Race', values='Percentage', 
                  title='Race Distribution',
                  color_discrete_sequence=colors)
race_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent', hole=.4)
race_pie.update_layout(title_font_size=11, font_size=9)

income_pie = px.pie(income_data, names='Income Range', values='Percentage', 
                    title='Income Distribution',
                    color_discrete_sequence=colors)
income_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent', hole=.4)
income_pie.update_layout(title_font_size=11, font_size=9)

sensitive_areas_pie = px.pie(sensitive_areas_data, names='Sensitive Areas', values='Density', 
                             title='Density of Sensitive Areas',
                             color_discrete_sequence=colors)
sensitive_areas_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent', hole=.4)
sensitive_areas_pie.update_layout(title_font_size=11, font_size=6)

app.layout = html.Div([

    # Row for Map Types and Noise Data (Left Section)
    html.Div([
        # Map Types Section
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
                style={'margin-bottom': '20px'}
            ),
            html.Label('Sensitive Areas'),
            dcc.Dropdown(
                options=[{'label': 'Churches', 'value': 'Churches'},
                        {'label': 'Hospitals/Medical Centers', 'value': 'Hospitals/Medical Centers'},
                        {'label': 'Schools/Universities', 'value': 'Schools/Universities'},],
                value=[],
                multi=True,
                style={'margin-bottom': '20px'}
            )
        ], style={'padding': 10, 'flex': 1, 'border': '1px solid #d3d3d3'}),

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
            html.Label('Noise Level Per Tract'),
            dcc.Slider(
                min=0,
                max=80,
                step=1,
                marks={i: f'{i} dB' for i in range(0, 81, 20)},
                value=40
            )
        ], style={'padding': 10, 'flex': 1, 'border': '1px solid #d3d3d3'})

    ], style={'display': 'flex', 'flexDirection': 'row'}),

    # Row for Pie Charts (Right Section)
    html.Div([
        html.Div([
            dcc.Graph(figure=race_pie)
        ], style={'width': '33%', 'display': 'inline-block', 'padding': 20}),
        
        html.Div([
            dcc.Graph(figure=income_pie)
        ], style={'width': '33%', 'display': 'inline-block', 'padding': 20}),
        
        html.Div([
            dcc.Graph(figure=sensitive_areas_pie)
        ], style={'width': '33%', 'display': 'inline-block', 'padding': 5}),
    ], style={'display': 'flex', 'justify-content': 'space-between'})

])

if __name__ == '__main__':
    app.run(debug=True)
