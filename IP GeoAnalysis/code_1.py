import pandas as pd
import array as arr
#reaading the dataset
file = pd.read_csv("webtraffic.csv")
#print(file)

country_code_to_name = {
    'US': 'United States',
    'CA': 'Canada',
    'GB': 'United Kingdom',
    'DE': 'Germany',
    'NL': 'Netherlands',
    'AE': 'United Arab Emirates',
    'AT': 'Austria',
    'IL': 'Israel'

}
file['country'] = file['src_ip_country_code'].map(country_code_to_name)
country_counts = file['country'].value_counts().reset_index()
country_counts.columns = ['country', 'connection_count']
print((country_counts)," ", (country_counts.columns))

import plotly.express as px

fig = px.choropleth(
    country_counts,
    locations="country",
    locationmode="country names",
    color="connection_count",
    color_continuous_scale="Viridis",
    title="Geographical Distribution of Source IP Addresses"
)
fig.show()
import folium
from folium.plugins import HeatMap
import Nominatim

# Create a base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Adding country counts to the map
for i, row in country_counts.iterrows():
    country = row['country_name']
    connections = row['connection_count']
    
    # Geocode the country name to get its latitude and longitude
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(country)

    if location:
        folium.CircleMarker(
            location=[location.latitude, location.longitude],
            radius=connections * 0.1, # scale radius
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)

# Save the map to an HTML file
m.save('ip_geolocation_map.html')