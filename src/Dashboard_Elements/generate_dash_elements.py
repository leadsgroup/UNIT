from dash import dcc
import dash_bootstrap_components as dbc


def color_switch():
    return   dbc.Row([
            dbc.Col([
                dbc.Label("Theme:", style={"font-weight": "bold"}, id="theme-label"),
                dcc.RadioItems(
                    id="theme-switch",
                    options=[
                        {"label": "Light", "value": "light"},
                        {"label": "Dark", "value": "dark"}
                    ],
                    value="dark",
                    inline=True,
                    style={'color': '#f7b731'}  # Highlighted color for better contrast
                ),
            ], width="auto", align="center")])