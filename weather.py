import requests
import folium
import streamlit as st
from folium import plugins


# Major cities and known grid points in Texas
texas_coordinates = [
    (29.7604, -95.3698),  # Houston
    (32.7767, -96.7970),  # Dallas
    (30.2672, -97.7431),  # Austin
    (29.4241, -98.4936),  # San Antonio
    (31.9686, -99.9018),  # Central Texas
    (33.7490, -101.8552), # Lubbock
    (31.7619, -106.4850), # El Paso
    # Add more if needed
]

def fetch_grid_data(latitude, longitude):
    """Fetch forecast grid data for a specific coordinate."""
    base_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        grid_data = response.json()
        
        # Check if the forecastGridData URL exists
        grid_forecast_url = grid_data['properties'].get('forecastGridData')
        if not grid_forecast_url:
            print(f"No forecast grid data available for ({latitude}, {longitude})")
            return None

        grid_forecast_response = requests.get(grid_forecast_url)
        grid_forecast_response.raise_for_status()
        grid_forecast_data = grid_forecast_response.json()
        
        # Get wind speeds from grid forecast data
        wind_speeds = grid_forecast_data['properties']['windSpeed']['values']
        return wind_speeds
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for ({latitude}, {longitude}): {http_err}")
    except Exception as e:
        print(f"Error fetching grid data for ({latitude}, {longitude}): {e}")
    return None

def fetch_texas_turbines():
    """Fetch wind turbine data for Texas."""
    url = "https://eersc.usgs.gov/api/uswtdb/v1/turbines?t_state=eq.TX"
    try:
        response = requests.get(url)
        response.raise_for_status()
        turbines = response.json()
        return turbines
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as e:
        print(f"Error fetching turbine data: {e}")
    return []

# Function to create a color-coded folium map for Texas
def create_wind_speed_map():
    wind_map = folium.Map(location=[31.5, -99.5], zoom_start=6)  # Centered on Texas
    
    # Fetch wind turbine data
    turbines = fetch_texas_turbines()
    turbine_locations = [(turbine['ylat'], turbine['xlong']) for turbine in turbines]

    # Filter turbines using a grid-based approach
    grid_size = 0.5  # Define grid size for filtering (in degrees)
    selected_turbines = {}
    
    for lat, lon in turbine_locations:
        grid_key = (round(lat / grid_size), round(lon / grid_size))
        if grid_key not in selected_turbines:
            selected_turbines[grid_key] = (lat, lon)

    # Fetch wind data for filtered turbine locations
    for lat, lon in selected_turbines.values():
        wind_speeds = fetch_grid_data(lat, lon)
        if wind_speeds:
            # Use the first wind speed value as representative
            wind_speed_value = wind_speeds[0]['value']
            
            # Define color based on wind speed ranges
            if wind_speed_value < 10:
                color = 'blue'
            elif 10 <= wind_speed_value < 20:
                color = 'green'
            elif 20 <= wind_speed_value < 30:
                color = 'orange'
            else:
                color = 'red'
            
            folium.CircleMarker(
                location=(lat, lon),
                radius=5,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=f"Wind Speed: {wind_speed_value} mph"
            ).add_to(wind_map)

    # Add a legend using a custom HTML element
    legend_html = '''
     <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: 120px;
                  background-color: white; border:2px solid grey; z-index:9999; font-size:14px;">
     &nbsp; <b>Wind Speed (mph)</b> <br>
     &nbsp; <i class="fa fa-circle" style="color:blue"></i>&nbsp; 0-10 <br>
     &nbsp; <i class="fa fa-circle" style="color:green"></i>&nbsp; 10-20 <br>
     &nbsp; <i class="fa fa-circle" style="color:orange"></i>&nbsp; 20-30 <br>
     &nbsp; <i class="fa fa-circle" style="color:red"></i>&nbsp; 30+ <br>
      </div>
     '''
    wind_map.get_root().html.add_child(folium.Element(legend_html))
    
    return wind_map

# Streamlit to display the map
st.title("Texas Wind Speed Map")
st.write("Color-coded map displaying wind speeds and wind turbine locations across Texas.")

# Generate and display the map
wind_speed_map = create_wind_speed_map()
wind_speed_map.save("wind_speed_map.html")
st.components.v1.html(open("wind_speed_map.html", "r").read(), height=500)
