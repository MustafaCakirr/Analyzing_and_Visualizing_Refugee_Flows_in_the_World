import pyodbc as db
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
from sql_connection import get_connection
from interactive_map import *

def total_ref_map():
       conn = get_connection()
       query = "SELECT * FROM [United Nations Refugee Data]"

       refugee_df = pd.read_sql(query, conn)    
       refugee_df = refugee_df[['Year', 'Country_of_origin', 'Country_of_asylum', 'Asylum_seekers']]
       refugee_df['Country_of_origin'] = refugee_df['Country_of_origin'].str.strip().str.lower()
       refugee_df['Country_of_asylum'] = refugee_df['Country_of_asylum'].str.strip().str.lower()
       refugee_df['Asylum_seekers'] = pd.to_numeric(refugee_df['Asylum_seekers'], errors='coerce')     
       refugee_summary = refugee_df.groupby('Country_of_asylum', as_index=False)['Asylum_seekers'].sum()
      
       shapefile_path = "C:/Users/MUSTAFA ÇAKIR/OneDrive/Masaüstü/Yeni klasör/ne_110m_admin_0_countries.shp"
       world = gpd.read_file(shapefile_path)     
       world['NAME'] = world['NAME'].str.strip().str.lower() 
       
       # merged = world.merge(refugee_df, how='left', left_on='NAME', right_on='Country_of_asylum')
       merged = world.merge(refugee_summary, how='left', left_on='NAME', right_on='Country_of_asylum')
          
       fig, ax = plt.subplots(1, 1, figsize=(16, 15))         
       merged.plot(
           column='Asylum_seekers', 
           ax=ax, 
           legend=True, 
           cmap='YlGnBu',  
           legend_kwds={
               'label': "Number of Asylum Seekers", 
               'orientation': "horizontal",
               'shrink': 0.6  
           },
           vmax=400000,  
           vmin=0   
       )       
       world.boundary.plot(ax=ax, color='lightgrey')     
       ax.set_title("Global Distribution of Asylum Seekers ", fontsize=15, fontweight='bold')
       ax.axis('off')  #       
       plt.show()
 
       interactive_map_html(merged)


