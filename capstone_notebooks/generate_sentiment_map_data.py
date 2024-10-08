import pandas as pd
import geopandas as gpd
import time

# Reduce dataframe size, takes too long
sentiment_df = pd.read_csv('../covid_sentiment_data.csv').head(10000)

# Initialize blank geodataframe
sentiment_locations = gpd.GeoDataFrame(columns=['address', 'geometry'], crs='EPSG:4326')

# Can't use lambda due to timeout issues
for index, row in sentiment_df.iterrows():
    try:
        # Attempt geocode on provided location
        geocodedf = gpd.tools.geocode(row['place'])

        # Attach sentiment
        geocodedf['sentiment'] = row['sentiment']

        # Add to initialized dataframe
        sentiment_locations = pd.concat([sentiment_locations, geocodedf], ignore_index=True)
    except Exception as e:

        # Error most likely due to rate limiting
        print(f"Error row: {index} geocoding {row['place']}: {e}")
        time.sleep(1)

# Store data
sentiment_locations.to_csv('sentiment_map_data.csv', index=False)
