# me397m-final-project
https://maxcarriker-me397m-final-project-weather2-jnb3x0.streamlit.app/

This is a Streamlit-based application that visualizes wind speed and direction data for a given state in the USA. The app generates an interactive map using Folium, displaying vectors that represent wind speeds and directions at selected turbine locations. The map also includes color-coded legends to indicate wind speed ranges.

## Features

- Fetch wind turbine data for a specified U.S. state.
- Display vectors for wind speed and direction on an interactive map.
- Customize the map by selecting grid sizes to filter turbine locations.
- Includes a dynamic progress bar to show the data-fetching process.
- Provides a legend for easy interpretation of wind speeds.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or later
- Required Python libraries listed in `requirements.txt`:
  ```
  folium
  streamlit
  requests
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/me397m-final-project.git
   cd me397m-final-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run weather2.py
   ```

2. Open the app in your browser using the URL provided in the terminal (default is `http://localhost:8501`).

3. Enter the state abbreviation (e.g., `TX` for Texas) and select the grid size to customize the visualization.

4. Click the "Generate Map" button to display the wind speed and direction map.

## How It Works

1. **Fetch Data:**
   - Uses the U.S. Wind Turbine Database API to retrieve turbine locations for the specified state.
   - Uses the National Weather Service API to fetch wind speed and direction data.

2. **Filter Locations:**
   - Filters turbine locations based on the selected grid size to avoid cluttering the map.

3. **Generate Map:**
   - Displays wind vectors using Folium's `PolyLine` for each turbine location.
   - Adds arrowheads to represent wind direction.

4. **Interactive Map:**
   - Allows users to explore wind patterns interactively.

## Example Output

- Wind vectors showing speed and direction.
- Color-coded lines to indicate wind speed ranges:
  - Blue: < 10 mph
  - Green: 10 - 20 mph
  - Orange: 20 - 30 mph
  - Red: > 30 mph
- Legend for easy interpretation of wind speed.

## Deployment

To deploy the app using Streamlit Cloud:

1. Push the repository to your GitHub account.
2. Ensure the `requirements.txt` file lists all dependencies.
3. Deploy via the Streamlit Cloud platform, linking to your GitHub repository.

## Troubleshooting

- **Error:** `ModuleNotFoundError: No module named 'folium'`
  - Ensure `folium` is listed in `requirements.txt` and run `pip install -r requirements.txt`.

- **API Issues:**
  - Verify API endpoints are accessible and functioning.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

