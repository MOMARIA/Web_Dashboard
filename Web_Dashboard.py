import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen
import requests

# Load the data and preprocess it
# Read the dataset from CSV
df = pd.read_csv("DATABASE.csv")

# Rename the 'nameOfFeature' column to 'nameOfFacility'
df.rename(columns={'nameOfFeature': 'nameOfFacility'}, inplace=True)

# Convert total pollutant quantity from Kg to MegaTonne
df["totalPollutantQuantityMegaTonne"] = df["totalPollutantQuantityKg"] / 1000000000

# Drop the original 'totalPollutantQuantityKg' column
df.drop(columns=["totalPollutantQuantityKg"], inplace=True)

# Filter data for medium 'AIR' and pollutant name 'Carbon dioxide'
df = df[(df["medium"] == "AIR") & (df["pollutantName"] == "Carbon dioxide")].reset_index(drop=True)

# Extract the short name of the method
df['methodShortName'] = df['methodName'].str.split(':').str[0]

# Drop unnecessary columns
df.drop(columns=["parentCompanyName", "AccidentalPollutantQuantityKG", "methodName"], inplace=True)

# Convert 'reportingYear' and 'city' columns to string type
df['reportingYear'] = df['reportingYear'].astype(str)
df['city'] = df['city'].astype(str)

# Group by 'nameOfFacility' and aggregate data
grouped = df.groupby('nameOfFacility').agg(
    Mean_totalPollutantQuantityMegaTonne=('totalPollutantQuantityMegaTonne', 'mean'),
    mainActivityName=('mainActivityName', 'first'),
    pointGeometryLon=('pointGeometryLon', 'first'),
    pointGeometryLat=('pointGeometryLat', 'first')
).reset_index()

polygons = requests.get(
    "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/1_deutschland/1_sehr_hoch.geo.json"
).json()

# Initial map and bar chart creation
initial_facility = "AGR mbH"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Facilities and their Pollutant Quantity in Germany"),
    html.Div([
        dcc.Graph(id='map', clickData={'points': [{'hovertext': initial_facility}]}),  # Initial clickData set to default facility
        html.Div(id='main-activity', style={'margin-left': '100px', 'display': 'inline-block', 'vertical-align': 'top', 'width': '600px'})
    ], style={'display': 'flex'}),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    [Output('map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('main-activity', 'children')],
    [Input('map', 'clickData')]
)
def update_output(clickData):
    facility = clickData['points'][0]['hovertext']
    
    # Update map
    fig_map = px.choropleth(
        geojson=polygons,
        locations=[feature['id'] for feature in polygons['features']],
        color_discrete_sequence=["lightgray"],
        projection='miller',
        title="Facilities and their Pollutant Quantity in Germany"
    )

    fig_map.add_trace(
        px.scatter_geo(
            grouped,
            lon='pointGeometryLon',
            lat='pointGeometryLat',
            size='Mean_totalPollutantQuantityMegaTonne',
            color='Mean_totalPollutantQuantityMegaTonne',   # Color bubbles based on CO2 emission
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=30,
            hover_name='nameOfFacility',
            hover_data=['Mean_totalPollutantQuantityMegaTonne', "mainActivityName"],
            title="Facility Pollutant Quantities"
        ).data[0]
    )

    fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    fig_map.update_geos(fitbounds="locations", visible=False)
    
    # Update bar chart
    fig_bar = px.bar(df[df['nameOfFacility'] == facility], 
                     x='reportingYear', 
                     y='totalPollutantQuantityMegaTonne', 
                     color='methodShortName', 
                     title=f"Total CO2 Quantity (MegaTonne) vs Reporting Year for {facility}",
                     labels={'totalPollutantQuantityMegaTonne': 'Total CO2 Quantity (MegaTonne)', 'reportingYear': 'Reporting Year'},
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     text_auto=True)
    fig_bar.update_layout(bargap=0.6)
    fig_bar.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    main_activity = f"Main Activity for {facility}: {grouped[grouped['nameOfFacility'] == facility]['mainActivityName'].iloc[0]}"
    
    return fig_map, fig_bar, main_activity

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
