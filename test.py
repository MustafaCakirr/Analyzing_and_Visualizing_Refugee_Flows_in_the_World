import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
from branca.colormap import LinearColormap
import numpy as np 
import pyodbc as db
import geopandas as gpd
import matplotlib.pyplot as plt
from sql_connection import get_connection

class RefugeeInteractiveMap:
    def __init__(self, conn):
        self.conn = conn

    def fetch_data(self, start_year, end_year):
        query = f"""
        SELECT Year, Country_of_origin, Country_of_asylum, Asylum_seekers
        FROM [United Nations Refugee Data]
        WHERE Year BETWEEN {start_year} AND {end_year}
        """
        df = pd.read_sql_query(query, self.conn)
        df['Asylum_seekers'] = pd.to_numeric(df['Asylum_seekers'], errors='coerce')
        return df

    def create_interactive_map(self, start_year, end_year):
        # Veriyi al
        df = self.fetch_data(start_year, end_year)

        # Harita başlangıç noktası ve zoom seviyesi
        refugee_map = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodbpositron')

        # Yoğunluk haritası için hazırlık
        heat_data = [
            [row['Latitude_asylum'], row['Longitude_asylum'], row['Asylum_seekers']]
            for _, row in df.iterrows() if not pd.isnull(row['Latitude_asylum']) and not pd.isnull(row['Longitude_asylum'])
        ]

        # Yoğunluk haritasını ekle
        HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(refugee_map)

        # Hareket oklarını ekle
        for _, row in df.iterrows():
            if not pd.isnull(row['Latitude_origin']) and not pd.isnull(row['Longitude_origin']) and \
               not pd.isnull(row['Latitude_asylum']) and not pd.isnull(row['Longitude_asylum']):
                folium.PolyLine(
                    locations=[
                        [row['Latitude_origin'], row['Longitude_origin']],
                        [row['Latitude_asylum'], row['Longitude_asylum']]
                    ],
                    color='blue',
                    weight=2,
                    opacity=0.5
                ).add_to(refugee_map)

        # Pop-up bilgilerini ekle
        for _, row in df.iterrows():
            if not pd.isnull(row['Latitude_asylum']) and not pd.isnull(row['Longitude_asylum']):
                folium.Marker(
                    location=[row['Latitude_asylum'], row['Longitude_asylum']],
                    popup=folium.Popup(
                        f"""
                        <b>Year:</b> {row['Year']}<br>
                        <b>Origin:</b> {row['Country_of_origin']}<br>
                        <b>Asylum:</b> {row['Country_of_asylum']}<br>
                        <b>Asylum Seekers:</b> {int(row['Asylum_seekers']) if pd.notnull(row['Asylum_seekers']) else 'N/A'}
                        """,
                        max_width=300
                    ),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(refugee_map)

        # Renk haritası ekle (isteğe bağlı)
        colormap = LinearColormap(
            colors=['green', 'yellow', 'red'],
            vmin=df['Asylum_seekers'].min(),
            vmax=df['Asylum_seekers'].max(),
            caption='Number of Asylum Seekers'
        )
        colormap.add_to(refugee_map)

        # Haritayı kaydet
        refugee_map.save("refugee_interactive_map.html")
        print("Harita 'refugee_interactive_map.html' dosyasına kaydedildi.")

# Kullanım
# conn: Veritabanı bağlantısı
# start_year, end_year: Verilerin çekileceği yıl aralığı


