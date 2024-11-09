from dash import dcc


def vertiports_checklist():
    return dcc.Checklist(
        options=[{'label': 'Vertiports', 'value': 'Vertiports'}],
        value=['Vertiports'],
        style={'margin-bottom': '10px'}
    )

def evtol_dropdown():
    return dcc.Dropdown(
                options=[
                    {'label': 'Stopped Rotor', 'value': 'Stopped Rotor'},
                    {'label': 'Tilt Rotor', 'value': 'Tilt Rotor'},
                    {'label': 'Hexacopter', 'value': 'Hexacopter'},
                ],
                value='Stopped Rotor',
                style={'margin-bottom': '20px'}
            )
def noise_type_dropdown():
    return dcc.Dropdown(
                id='noise_type_dropdown',
                options=[
                    {'label': 'L_AeqT', 'value': 'L_AeqT'},
                    {'label': 'L_AeqT_24hr', 'value': 'L_AeqT_24hr'},
                    {'label': 'SEL', 'value': 'SEL'},
                    {'label': 'L_dn', 'value': 'L_dn'},
                    {'label': 'L_Aeq_jetliner', 'value': 'L_Aeq_jetliner'},
                    {'label': 'L_Amax', 'value': 'L_Amax'}
                ],
                value='L_AeqT',
                style={'margin-bottom': '20px'}
            )
def noise_slider():
    return dcc.Slider(
                id='noise_level_slider',
                min=0,
                max=80,
                step=1,
                marks={i: f'{i} dB' for i in range(0, 81, 20)},
                value=40)