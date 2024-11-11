from dash import dcc
import dash_bootstrap_components as dbc


def color_switch():
    return   dbc.Row([
            dbc.Col([
                dbc.Label("Theme:", style={"font-weight": "bold"}, id="theme-label"),
                dcc.RadioItems(
                    id="theme-switch",
                    options=[
                        {"label": "Light ", "value": "light"},
                        {"label": "Dark", "value": "dark"}
                    ],
                    value="dark",
                    inline=True,
                    style={'color': '#f7b731'}  # Highlighted color for better contrast
                ),
            ], width="auto", align="center")])

def update_theme(selected_theme):
    # Define light and dark theme styles
    if selected_theme == "light":
        container_style = {"backgroundColor": "#f9f9f9", "color": "#2d2d2d"}
        header_style = {"color": "#1a1a1a", "font-weight": "bold"}
        label_style = {"color": "#333333", "font-weight": "bold"}
        card_header_style = {"color": "#ffffff", "backgroundColor": "#007bff"}
    else:
        container_style = {"backgroundColor": "#1e1e1e", "color": "#ffffff"}
        header_style = {"color": "#f0f0f0", "font-weight": "bold"}
        label_style = {"color": "#00aaff", "font-weight": "bold"}
        card_header_style = {"color": "#00aaff", "backgroundColor": "#007bff"}

    return (
        container_style,  # app-container
        header_style,     # app-title
        label_style,      # theme-label
        label_style,      # evtol-label
        label_style,      # noise-type-label
        label_style,      # noise-level-label
        container_style,    # noise -controls-section
        container_style     #pie-chart-section

    )
