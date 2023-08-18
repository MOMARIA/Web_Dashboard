# Web Dashboard for CO2 Emissions Data

This project is a web dashboard that visualizes German CO2 emissions data in a map and charts using Python and the Dash framework. It allows users to explore pollution data interactively.

## Deployment

The web app is deployed on Render and can be accessed at:
[https://de-co2-dashboard.onrender.com](https://de-co2-dashboard.onrender.com)

## Data Source

## Data Source

The pollution data used in this project comes from the European Environment Agency (EEA). It contains information about the total quantity of pollutants released by various facilities, categorized by medium and pollutant type.

- Data Source: [EEA Data Hub](https://www.eea.europa.eu/en/datahub/datahubitem-view/9405f714-8015-4b5b-a63c-280b82861b3d)

## GeoJSON Data

The map visualizations are generated using GeoJSON data for Germany's administrative regions.

- GeoJSON Source: [deutschlandGeoJSON](https://github.com/isellsoap/deutschlandGeoJSON/tree/main/1_deutschland)

## Requirements

To run the web dashboard locally, you must install the required Python packages. You can install them using the `requirements.txt` file in the repository.

```
pip install -r requirements.txt
```

## Running the Dashboard

To run the web dashboard, execute the `Web_Dashboard.py` script:

```
python Web_Dashboard.py
```

The dashboard will be accessible in your web browser at `http://127.0.0.1:8050/`.
