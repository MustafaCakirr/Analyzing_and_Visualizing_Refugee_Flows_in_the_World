from matplotlib import interactive
import pandas as pd 
import numpy as np 
import pyodbc as db
import geopandas as gpd
import matplotlib.pyplot as plt
from sql_connection import get_connection
import folium
from interactive_map import *

class WorldRefugeeMap:
    def __init__(self,conn):
        self.conn = conn

    def world_data_visualizer(self,data1,data2 = None):
        max  = 0 
        if data2:
            query = f"SELECT * FROM [United Nations Refugee Data] WHERE Year  BETWEEN  {data1} AND {data2}"
        elif data2 is None: 
            query = f"SELECT * FROM [United Nations Refugee Data] WHERE  Year >= {data1}"
            if (0 <= (2022 - data1) <= 5):
                max = 30000
            elif ( 6 <= (2022 - data1) <= 10):
                max = 35000
            elif (11 <= (2022 - data1) <= 15):
                max = 40000
            elif (16 <= (2022 - data1) <= 20):
                max = 45000
            elif (21 <= (2022 - data1) <= 30):
                max = 55000
            elif ((2022 - data1) >= 31 ):
                max = 65000
   
        refugee_df = pd.read_sql_query(query, self.conn)
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

        if ((data2 is not None) and ( 0 <= (data2 - data1) <= 3)) :  
            max = 25000
                
        elif (data2 is not None and ( 4 <= (data2 - data1) <= 7)):
            max = 30000            
        elif (data2 is not None and ( 7 <= (data2 - data1) <= 11)):
            max = 35000
        elif (data2 is not None and ((data2 - data1) >= 12 )):
            max = 45000
     
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
        vmax=max, 
        vmin=0  
        )
        world.boundary.plot(ax=ax, color='lightgrey')
        ax.set_title("Global Distribution of Asylum Seekers ", fontsize=15, fontweight='bold')
        ax.axis('off')        
        plt.show()
    
        if data2:
            interactive_map_html(merged,data1,data2)
        elif data2 is None: 
            interactive_map_html(merged,data1)
        
        self.plot_time_series(refugee_df) 
       
    def plot_time_series(self,refugee_df):
        time_series_data = refugee_df.groupby('Year')['Asylum_seekers'].sum().reset_index()
        refugee_df = refugee_df.dropna(subset=['Year', 'Asylum_seekers'])

        plt.figure(figsize=(18,9))
        plt.plot(
            time_series_data['Year'],
            time_series_data['Asylum_seekers'],
            marker = 'o',
            color = 'skyblue',
            label = 'Total Asylum Seekers'
        )
        plt.title('Number of Asylum Seekers Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('Number of Asylum Seekers', fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(time_series_data['Year'], rotation=45, fontsize=12)
        plt.legend()
        plt.tight_layout()
        plt.show()
              
world_data_visiualizer = WorldRefugeeMap(get_connection()).world_data_visualizer


                

