import pandas as pd

""" Bastırılacak verilerin tümünü görmek için pandas dataframe'lerinin satır sınırını kaldırma """
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)