# Analyzing_and_Visualizing_Refugee_Flows_in_the_World
## Languages Used
- **Python**: Data processing, analysis, and visualization.
- **SQL**: Database management and querying.

  This project aims to visualize the global distribution of asylum seekers, their changes over years, and filtered data for specific countries using United Nations Refugee Data. It includes both static visualizations (with matplotlib) and interactive map applications (with folium).

## Features
- **Global Distribution Visualization:**
  - Summarization of asylum seeker numbers by country based on the "United Nations Refugee Data" table from SQL Server
  - Visualization of asylum seeker density using color scales by merging data with country geographic boundaries via Shapefiles
    
- **Interactive Map:**
  - Creation of interactive choropleth maps using the Folium library
  - Detailed information display through country-specific markers on the map
  - Saving generated maps as HTML files
    
- **Time Series Analysis:**
  - Aggregation of asylum seeker numbers by year and visualization of trends using matplotlib
  - Detailed analysis through filtering by specific countries or year ranges

- **Modular Structure:**
  - Readable and maintainable code through purpose-specific modules
 
## Key Functions

### 1. Global Density Map Generation
- from total_refugee_density_map import total_ref_map
- total_ref_map()

- **Functionality:**
  - Generates a comprehensive refugee density map covering all years. Analyzes all records in the database to show total refugee density per country.
- **Outputs:**
  - Static heatmap using Matplotlib
  - Interactive HTML map using Folium
    
### 2. Time-Based Analysis
- from world_data_visualization import world_data_visiualizer
- world_data_visiualizer(2000, 2020) # For specific year range
- world_data_visiualizer(2021) # For single year

- **Functionality:**
  - Analyzes refugee movements during specified year range. Generates time series charts and year-specific colored maps.
- **Outputs:**
  - Annual change chart (Matplotlib)
  - Interactive map tailored to selected year range

### 3. Country-Specific Filtering
- from filtered_refugee_class import filtered_year_and_country
- filtered_year_and_country(1990, 2022, "Turkey")
  
- **Functionality:**
  - Performs detailed analysis for specific countries and year ranges. Shows both refugee distribution and temporal changes  for target countries.
- **Outputs:**
  - Country-specific heatmap
  - Annual change chart
