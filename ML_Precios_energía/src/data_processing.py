import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# Leo data set del precio de la energía (variable objetivo)
from pathlib import Path

RAW_DIR = Path().resolve().parent / 'data' / 'raw'

dfp1 = pd.read_csv(RAW_DIR / '202401CmgBarras.csv', sep=';', decimal=',')
dfp2 = pd.read_csv(RAW_DIR / '202402CmgBarras.csv', sep=';', decimal=',')
dfp3 = pd.read_csv(RAW_DIR / '202403CmgBarras.csv', sep=';', decimal=',')
dfp4 = pd.read_csv(RAW_DIR / '202404CmgBarras.csv', sep=';', decimal=',')
dfp5 = pd.read_csv(RAW_DIR / '202405CmgBarras.csv', sep=';', decimal=',')
dfp6 = pd.read_csv(RAW_DIR / '202406CmgBarras.csv', sep=';', decimal=',')
dfp7 = pd.read_csv(RAW_DIR / '202407CmgBarras.csv', sep=';', decimal=',')
dfp8 = pd.read_csv(RAW_DIR / '202408CmgBarras.csv', sep=';', decimal=',')
dfp10 = pd.read_csv(RAW_DIR / '202410CmgBarras.csv', sep=';', decimal=',')
dfp11 = pd.read_csv(RAW_DIR / '202411CmgBarras.csv', sep=';', decimal=',')
dfp12 = pd.read_csv(RAW_DIR / '202412CmgBarras.csv', sep=';', decimal=',')


#Concateno los DataFrames en el orden deseado
dfp = pd.concat([dfp1, dfp2, dfp3, dfp4, dfp5, dfp6, dfp7, dfp8, dfp10, dfp11, dfp12], ignore_index=True)


# Filtro sólo los valores de crucero
filtro1 = 'CRUCERO_______220'
dfp = dfp[(dfp['barra'] == filtro1)]

# Lo guardo solo con el nombre de la ciudad
dfp['barra'] = dfp['barra'].replace({'CRUCERO_______220': 'crucero'})


# Cargo los datos de los archivos meteorológicos
RAW_DIR = Path().resolve().parent / 'data' / 'raw'
dfm = pd.read_excel(RAW_DIR / 'meteo_crucero_2024_NSRDB.xlsx', skiprows=2)


# Me quedo con las primeras 27 columnas que tienen informacion
dfm = dfm.iloc[:, :28]

# Elimino los valores de septiembre, porque no tengo el target de ese mes
dfm = dfm[dfm['Month'] != 9]

# Corrijo formato hora
dfm['Hour'] = dfm['Hour'] + 1

df = pd.merge(
    dfm,
    dfp,
    left_on=['Month', 'Day', 'Hour'],
    right_on=['mes', 'dia', 'hora'],
    how='left'
)

# Voy a eliminar las columnas temporales duplicadas
df = df.drop(columns=['mes', 'dia', 'hora'])

# Voy a eliminar las columnas de texto que no me sirve
df = df.drop(columns=['fecha','barra'])

# Eliminar los valores Nan
df = df.dropna()

# CANTIDAD DE REGISTROS *****************
# Tengo 9500 registros, voy a reducir a la mitad y tomar 5000
df = df[:5000]


# Selecciono variables relevantes de acuerdo al análisis
variables = ['Month','Day','Temperature', 'Hour','Aerosol Optical Depth','Dew Point','DHI', 'DNI', 'GHI',
              'Relative Humidity', 'Solar Zenith Angle', 'Pressure', 'Precipitable Water', 'Wind Direction', 'valor']

df2 = df[variables]

# Guardo el data set procesado
PROCESSED_DIR = Path().resolve().parent / 'data' / 'processed'
df2.to_csv(PROCESSED_DIR / 'meteo_processed.csv', index=False)

print('Dataset procesado ok')