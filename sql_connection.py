import pyodbc as db

# shapefile_path = "C:/Users/MUSTAFA ÇAKIR/OneDrive/Masaüstü/Yeni klasör/ne_110m_admin_0_countries.shp"
shapefile_path = "C:/Users/MUSTAFA CAKIR/OneDrive/Masaustu/Yeni klasor/ne_110m_admin_0_countries.shp"
def get_connection():
    return db.connect('DRIVER={SQL Server};'
                          'SERVER=DESKTOP-******\SQLEXPRESS;' # Enter your custom computer name in the starred area
                          'DATABASE=Refugee;'
                          'Trusted_Connection=True;')

