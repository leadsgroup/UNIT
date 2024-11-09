from dash import dcc


def noise_slider():
    return dcc.Slider(
                id='noise_level_pc',
                min=0,
                max=80,
                step=1,
                marks={i: f'{i} dB' for i in range(0, 81, 20)},
                value=40)

def noise_type():
    return dcc.Dropdown(
                id='noise_type_dropdown_pc',
                options=[
                    {'label': 'L_AeqT', 'value': 'L_AeqT'},
                    {'label': 'L_AeqT_24hr', 'value': 'L_AeqT_24hr'},
                    {'label': 'SEL', 'value': 'SEL'},
                    {'label': 'L_dn', 'value': 'L_dn'},
                    {'label': 'L_Aeq_jetliner', 'value': 'L_Aeq_jetliner'},
                    {'label': 'L_Amax', 'value': 'L_Amax'}
                ],
                value='L_AeqT',
                style={'margin-bottom': '20px'})