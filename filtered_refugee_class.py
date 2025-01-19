import time
from turtle import color
from matplotlib.lines import lineStyles
import pandas as pd 
import numpy as np 
import pyodbc as db
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
from sql_connection import get_connection

class RefugeeDataBase:
    def __init__(self,conn):
        self.conn = conn
       
    def fetch_data(self,start_year,end_year,country):
        query = f"SELECT * FROM [United Nations Refugee Data] WHERE  (Year >= {start_year} AND  Year <= {end_year}) AND Country_of_asylum LIKE '%{country}%' "
 
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
            vmax=30000,  
            vmin=0   
        )     
        world.boundary.plot(ax=ax, color='lightgrey')    
        ax.set_title("Global Distribution of Asylum Seekers ", fontsize=15, fontweight='bold')
        ax.axis('off')   
        plt.show()

        time_series_data = refugee_df.groupby('Year')['Asylum_seekers'].sum().reset_index()

        plt.figure(figsize=(14,7))
        plt.plot(
            time_series_data['Year'],
            time_series_data['Asylum_seekers'],
            marker = 'o',
            color = 'coral',
            label = f'Total Asylum Seekers in {country}'
            )
        plt.title(f'Asylum Seekers in {country} Over Time', fontsize = 16,fontweight = 'bold')
        plt.xlabel('Year',fontsize =14)
        plt.ylabel('Number of Asylum Seekers',fontsize = 14)
        plt.ylim(0,time_series_data['Asylum_seekers'].max()*1.1)
        plt.xticks(time_series_data['Year'],rotation = 45,fontsize =12)
        plt.yticks(fontsize = 12)
        plt.grid(axis='y',linestyle = '--',alpha = 0.7)
        plt.legend()
        plt.tight_layout()
        plt.show()

filtered_year_and_country = RefugeeDataBase(get_connection()).fetch_data



