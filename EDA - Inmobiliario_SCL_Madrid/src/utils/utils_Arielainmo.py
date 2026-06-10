import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from bootcampviztools import plot_combined_graphs, pinta_distribucion_categoricas, plot_categorical_relationship_fin,\
      plot_grouped_boxplots,plot_grouped_histograms, grafico_dispersion_con_correlacion, plot_categorical_numerical_relationship, bubble_plot
from scipy.stats import zscore

## FUNCIÓN PARA EDITAR CSV


def editar_csv(df_inm):
    #Correge la columna de precio, porque piensa que es un str. Elimino el signo $ y los puntos
    df_inm['precio'] = pd.to_numeric(df_inm['precio'].str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.strip()) 
    
    #Correge la columna de m2  
    df_inm['m2'] = pd.to_numeric(df_inm['m2'].str.replace(" m²", "", regex=False).str.replace(",", ".", regex=False))

    # Agrega una columna con el precio en euros
    df_inm['precio_eu'] = df_inm['precio']*0.00094
    
    # Elimina valores cero o menores 
    filtro = (df_inm.precio_eu> 1)&(df_inm.m2> 20)&(df_inm.precio_eu< 10000) #Hay algunos en LC que tenían 1m2
    df_inm = df_inm[filtro]

    # Genero la columna del indicador precio/m2
    df_inm['precioeu_m2'] = df_inm['precio_eu']/df_inm['m2']

    # Ordeno el csv
    df_inm = df_inm.rename(columns={"fecha": "fecha_pub"})
    df_inm = df_inm[["titulo", "m2","precio_eu","precioeu_m2","dormitorios","estacionamientos","fecha_pub"]]
  
    return df_inm


def filtrar_busqueda(df_inm,dorm,estac,m2_min,m2_max):
    
    filtro = (df_inm.dormitorios >= dorm)&(df_inm.estacionamientos >= estac)&(df_inm.m2 >= m2_min)&(df_inm.m2 <= m2_max)
    df_inm2 = df_inm[filtro]
    df_inm2
    
    return df_inm2


    # Análisis por grupo
def desc_gruposm2(df_inm):
      rangos = [0, 40, 60, 80,100,120, float('inf')]
      etiquetas = ['<40', '40-60', '60-80', '80-100','100-120','>120']
      df_inm['grupo_m2'] = pd.cut(df_inm['m2'], bins=rangos, labels=etiquetas)
      descripcion = df_inm.groupby('grupo_m2')['precioeu_m2'].describe()

      return descripcion


     


