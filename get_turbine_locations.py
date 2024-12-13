import requests
import csv

def fetch_texas_turbines():
    """Fetch wind turbine data for Texas."""
    url = "https://eersc.usgs.gov/api/uswtdb/v1/turbines?t_state=eq.TX"
    try:
        response = requests.get(url)
        response.raise_for_status()
        turbines = response.json()
        return turbines
    except requests.exceptions.RequestException as e:
        print(f"Error fetching turbine data: {e}")
        return []

def save_turbine_locations_to_csv(filename="turbine_locations.csv"):
    """Save wind turbine locations to a CSV file."""
    turbines = fetch_texas_turbines()
    turbine_locations = [(turbine['ylat'], turbine['xlong']) for turbine in turbines]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Latitude", "Longitude"])
        writer.writerows(turbine_locations)

    print(f"Turbine locations saved to {filename}")

# Save turbine locations to a CSV file
save_turbine_locations_to_csv()
