import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

# Load in combined sentiment + map data
df = pd.read_csv('../sentiment_map_data.csv')

# Drop rows with no location
df = df[df['geometry'] != 'POINT EMPTY']

# Define coordinate extraction function
def extract_coordinates(point):
    coords = point.replace('POINT (', '').replace(')', '').split()
    return float(coords[1]), float(coords[0])

# Apply extract_coordinates function to 'geometry' column and create 'Latitude' and 'Longitude' columns
df['Latitude'], df['Longitude'] = zip(*df['geometry'].apply(extract_coordinates))

# Create Point geometries from Latitude and Longitude columns
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

# Create a GeoDataFrame from original dataframe with Point geometries
latlong_gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Load in geo json for countries - defines Chloropleth bounds
countries_gdf = gpd.read_file('../countries.geojson')

# Match coordinates to country using CRS (Coordinate Reference System)
latlong_gdf = latlong_gdf.set_crs(countries_gdf.crs, allow_override=True)

# Combine countries GeoDataFrame with coordinate GeoDataFrame pass to folium
joined_gdf = gpd.sjoin(latlong_gdf, countries_gdf, how="left", op='within')

# Group dataframe rows by ADMIN (Standardized Country Name) and calculate average sentiment
country_data = joined_gdf.groupby('ADMIN')['sentiment'].mean().reset_index()

# Initialize map
m = folium.Map([20, 0], zoom_start=2)

# Add Chloropleth map
folium.Choropleth(
    geo_data=countries_gdf,
    data=country_data,
    columns=["ADMIN", "sentiment"],
    key_on="feature.properties.ADMIN",
    fill_color='RdBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average COVID-19 Sentiment'
).add_to(m)

# Save HTML
m.save('world_map_with_latlong_data.html')
