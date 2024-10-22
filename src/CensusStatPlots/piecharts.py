import pandas as pd
import plotly.express as px

def generate_pie_chart():
    # sample data for pie charts
    race_data = pd.DataFrame({
        'Race': ['Hispanic/Latino', 'Black/African American', 'White'],
        'Percentage': [30, 40, 30]
    })

    income_data = pd.DataFrame({
        'Income Range': [
            '0-30,000', '30,000-60,000', '60,000-90,000', '90,000-100,000'
        ],
        'Percentage': [30, 30, 25, 15]
    })

    sensitive_areas_data = pd.DataFrame({
        'Sensitive Areas': ['Churches', 'Hospitals/Medical Buildings', 'Schools/Universities'],
        'Density': [40, 35, 25]
    })

    # colors for the pie charts
    colors = ['#636EFA', '#EF553B', '#00CC96']

    # create pie charts with hover and uniform sizes
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

    return race_pie, income_pie, sensitive_areas_pie
