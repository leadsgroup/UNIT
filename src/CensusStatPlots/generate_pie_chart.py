import pandas as pd
import plotly.express as px

def generate_pie_chart(tract_number, race_data, income_data):
    race_data = gpd.read_file(r'C:/Users/avacipriani/Desktop/LEADS/UNIT/Processed_Data/data race la county/filtered_race_data_lacounty.geojson')
    income_data = gpd.read_file(r'C:/Users/avacipriani/Desktop/LEADS/UNIT/Processed_Data/data income la county/filtered_income_data_lacounty.geojson')
    # Filter for the specific tract
    race_tract = race_data[race_data['geoid'] == tract_number].iloc[0]
    income_tract = income_data[income_data['geoid'] == tract_number].iloc[0]
    
    # Race distribution: Hispanic/Latino, Black/African American, White
    race_distribution = {
        'Hispanic or Latino': race_tract['B03002012'],
        'Non-Hispanic Black or African American': race_tract['B03002004'],
        'Non-Hispanic White': race_tract['B03002003']
    }
    race_df = pd.DataFrame(list(race_distribution.items()), columns=['Race', 'Count'])
    
    # Income distribution: ranges up to $100,000 in increments of $10,000
    income_ranges = {
        '0-10,000': income_tract['B19001002'],
        '10,000-20,000': income_tract['B19001003'] + income_tract['B19001004'] ,
        '20,000-30,000': income_tract['B19001005'] + income_tract['B19001006'],
        '30,000-40,000': income_tract['B19001007'] + income_tract['B19001008'],
        '40,000-50,000': income_tract['B19001009'] + income_tract['B19001010'],
        '50,000-60,000': income_tract['B19001011'],
        '60,000-75,000': income_tract['B19001012'],
        '60,000-100,000': income_tract['B19001013'],
        '100,000 to 125,000': income_tract['B19001014'],
        '125,000 to 150,000': income_tract['B19001015'],
        '150,000-200,000': income_tract['B19001016']
    }
    income_df = pd.DataFrame(list(income_ranges.items()), columns=['Income Range', 'Count'])
    
    # Sample Sensitive Areas distribution (replace with actual data when available)
    sensitive_areas_data = pd.DataFrame({
        'Sensitive Areas': ['Churches', 'Hospitals/Medical Buildings', 'Schools/Universities'],
        'Density': [10, 15, 5]  # Example values; replace with actual counts per tract if available
    })
    
    # Generate pie charts
    race_pie = px.pie(race_df, names='Race', values='Count', title='Race Distribution')
    income_pie = px.pie(income_df, names='Income Range', values='Count', title='Income Distribution')
    sensitive_areas_pie = px.pie(sensitive_areas_data, names='Sensitive Areas', values='Density', 
                                 title='Density of Sensitive Areas')
    
    # Customize layout and appearance
    for pie_chart in [race_pie, income_pie, sensitive_areas_pie]:
        pie_chart.update_traces(textinfo='percent+label', hole=.4)
        pie_chart.update_layout(title_font_size=11, font_size=9)
    
    return race_pie, income_pie, sensitive_areas_pie
