import requests
import folium
import streamlit as st
import math

# Fetch grid data
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

        # Get wind speeds and directions from grid forecast data
        wind_speeds = grid_forecast_data['properties']['windSpeed']['values']
        wind_directions = grid_forecast_data['properties']['windDirection']['values']
        return wind_speeds, wind_directions
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for ({latitude}, {longitude}): {http_err}")
    except Exception as e:
        print(f"Error fetching grid data for ({latitude}, {longitude}): {e}")
    return None, None

# Fetch turbine data
def fetch_turbine_data(state):
    """Fetch wind turbine data for a specific state."""
    url = f"https://eersc.usgs.gov/api/uswtdb/v1/turbines?t_state=eq.{state.upper()}"
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

# Create color scale
def create_color_scale(wind_speed):
    """Determine color based on wind speed."""
    if wind_speed < 10:
        return "blue"
    elif 10 <= wind_speed < 20:
        return "green"
    elif 20 <= wind_speed < 30:
        return "orange"
    else:
        return "red"

# Create wind map
def create_wind_speed_map(turbine_locations, grid_size):
    wind_map = folium.Map(location=[31.5, -99.5], zoom_start=6)
    selected_turbines = {}

    # Filter turbines by grid size
    for lat, lon in turbine_locations:
        grid_key = (round(lat / grid_size), round(lon / grid_size))
        if grid_key not in selected_turbines:
            selected_turbines[grid_key] = (lat, lon)

    progress = st.progress(0)
    total = len(selected_turbines)

    # Fetch and display wind data
    for idx, (lat, lon) in enumerate(selected_turbines.values(), 1):
        wind_speeds, wind_directions = fetch_grid_data(lat, lon)
        if wind_speeds and wind_directions:
            wind_speed_value = wind_speeds[0]['value']
            length = wind_speed_value * 0.01

            # Calculate end point
            end_lat = lat + length * math.cos(math.radians(wind_directions[0]['value']))
            end_lon = lon + length * math.sin(math.radians(wind_directions[0]['value']))

            # Calculate arrowhead lines
            arrow_angle = 180+30  # Degrees for arrowhead
            arrow_length = 0.5 * length  # Length of the arrowhead lines
            left_angle = math.radians(wind_directions[0]['value'] + arrow_angle)
            right_angle = math.radians(wind_directions[0]['value'] - arrow_angle)

            left_lat = end_lat + arrow_length * math.cos(left_angle)
            left_lon = end_lon + arrow_length * math.sin(left_angle)
            right_lat = end_lat + arrow_length * math.cos(right_angle)
            right_lon = end_lon + arrow_length * math.sin(right_angle)

            # Draw main line
            color = create_color_scale(wind_speed_value)
            folium.PolyLine(
                locations=[(lat, lon), (end_lat, end_lon)],
                color=color,
                weight=2
            ).add_to(wind_map)

            # Draw arrowhead lines
            folium.PolyLine(
                locations=[(end_lat, end_lon), (left_lat, left_lon)],
                color=color,
                weight=2
            ).add_to(wind_map)

            folium.PolyLine(
                locations=[(end_lat, end_lon), (right_lat, right_lon)],
                color=color,
                weight=2
            ).add_to(wind_map)

        progress.progress(idx / total)

    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 150px; 
                background-color: white; z-index:9999; font-size:14px; 
                border:2px solid grey; padding: 10px;">
        <b>Wind Speed Legend</b><br>
        <i style="background:blue; width:20px; height:10px; display:inline-block;"></i> < 10 mph<br>
        <i style="background:green; width:20px; height:10px; display:inline-block;"></i> 10 - 20 mph<br>
        <i style="background:orange; width:20px; height:10px; display:inline-block;"></i> 20 - 30 mph<br>
        <i style="background:red; width:20px; height:10px; display:inline-block;"></i> > 30 mph<br>
    </div>
    '''
    wind_map.get_root().html.add_child(folium.Element(legend_html))

    return wind_map

# Streamlit app
st.title("Wind Speed and Direction Map")
st.write("Select parameters and generate the map.")

# User input
state = st.text_input("Enter state abbreviation (e.g., TX):", "TX")
grid_size = st.slider("Select grid size (degrees):", 0.1, 5.0, 0.5, 0.1)

if st.button("Generate Map"):
    turbines = fetch_turbine_data(state)
    turbine_locations = [(turbine['ylat'], turbine['xlong']) for turbine in turbines]
    wind_speed_map = create_wind_speed_map(turbine_locations, grid_size)
    wind_speed_map.save("wind_speed_map.html")
    st.components.v1.html(open("wind_speed_map.html", "r").read(), height=500)
