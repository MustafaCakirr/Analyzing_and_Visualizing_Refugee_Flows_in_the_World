import pyodbc as db

# shapefile_path = "C:/Users/MUSTAFA �AKIR/OneDrive/Masa�st�/Yeni klas�r/ne_110m_admin_0_countries.shp"
shapefile_path = "C:/Users/MUSTAFA CAKIR/OneDrive/Masaustu/Yeni klasor/ne_110m_admin_0_countries.shp"
def get_connection():
    return db.connect('DRIVER={SQL Server};'
                          'SERVER=DESKTOP-MET5ESU\SQLEXPRESS;'
                          'DATABASE=Refugee;'
                          'Trusted_Connection=True;')

