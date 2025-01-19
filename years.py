import pyodbc as db
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
from sql_connection import get_connection
 
def year_map(year1):
       conn = get_connection()
       query = f"SELECT * FROM [United Nations Refugee Data] WHERE  Year > {year1} "
       refugee_df = pd.read_sql(query, conn)
       
       # İlgili sütunların seçimi ve düzenleme
       refugee_df = refugee_df[['Year', 'Country_of_origin', 'Country_of_asylum', 'Asylum_seekers']]
       refugee_df['Country_of_origin'] = refugee_df['Country_of_origin'].str.strip().str.lower()
       refugee_df['Country_of_asylum'] = refugee_df['Country_of_asylum'].str.strip().str.lower()
       refugee_df['Asylum_seekers'] = pd.to_numeric(refugee_df['Asylum_seekers'], errors='coerce')
       
       # Toplam mülteci sayısının hesaplanması
       refugee_summary = refugee_df.groupby('Country_of_asylum', as_index=False)['Asylum_seekers'].sum()
       
       # Dünya haritasının şekil dosyasının okunması
       shapefile_path = "C:/Users/MUSTAFA ÇAKIR/OneDrive/Masaüstü/Yeni klasör/ne_110m_admin_0_countries.shp"
       world = gpd.read_file(shapefile_path)
       
       # Eşleştirme için ülke isimlerinin düzenlenmesi
       world['NAME'] = world['NAME'].str.strip().str.lower()
       
       # Verilerin birleştirilmesi
       # merged = world.merge(refugee_df, how='left', left_on='NAME', right_on='Country_of_asylum')
       merged = world.merge(refugee_summary, how='left', left_on='NAME', right_on='Country_of_asylum')
       
       
       fig, ax = plt.subplots(1, 1, figsize=(16, 15))
       
       # Yoğunluk haritası
       merged.plot(
           column='Asylum_seekers', 
           ax=ax, 
           legend=True, 
           cmap='YlGnBu',  # mavi renk skalası
           legend_kwds={
               'label': "Number of Asylum Seekers", 
               'orientation': "horizontal",
               'shrink': 0.6  # Lejant boyutunu küçült
           },
           vmax=30000,  # Maksimum yoğunluk değeri
           vmin=0   # Minimum yoğunluk değeri
       )
       
       # Sınır çizgileri
       world.boundary.plot(ax=ax, color='lightgrey')
       
       # Harita başlığı
       ax.set_title("Global Distribution of Asylum Seekers (Post-2000)", fontsize=15, fontweight='bold')
       ax.axis('off')  # Eksenleri gizle
       
       plt.show()
