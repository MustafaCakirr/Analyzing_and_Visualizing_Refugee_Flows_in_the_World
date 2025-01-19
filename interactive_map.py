import pandas as pd 
import geopandas as gpd
import folium

def interactive_map_html(merged,data1=None,data2 = None):  
    map_save = folium.Map(location=[0, 0], zoom_start=2)
   
    folium.Choropleth(
        geo_data=merged,
        data=merged,
        columns=['NAME', 'Asylum_seekers'],
        key_on='feature.properties.NAME',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Asylum Seekers'
    ).add_to(map_save)
    
    for _, row in merged.iterrows():
        if not pd.isna(row['Asylum_seekers']):  
            folium.Marker(
                location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
                popup=f"{row['NAME'].title()}: {int(row['Asylum_seekers']):,} asylum seekers"
            ).add_to(map_save)

    if data2:
        map_save.save(f'interactive_refugee_map{data1}_{data2}.html')
        print(f"Harita 'interactive_refugee_map{data1}_{data2}.html' olarak kaydedildi.")
    elif (data2 is None) and (data1): 
        map_save.save(f'interactive_refugee_map{data1}.html')
        print(f"Harita 'interactive_refugee_map{data1}.html' olarak kaydedildi.")
    elif (data2 is None) and (data1 is None):
        map_save.save('Total_refugee_density_map.html')
        print("Total_refugee_density'Total_refugee_density_map.html' olarak kaydedildi.")
    
