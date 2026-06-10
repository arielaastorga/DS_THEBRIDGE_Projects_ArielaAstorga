from utils_Arielainmo import editar_csv,filtrar_busqueda,desc_gruposm2
import pandas as pd

def main():
 
   # Análisis de CSV Lo Barnechea
   df_inm = pd.read_csv("EDA_Inmob_Lobarnechea.csv")

   df_inmlb = editar_csv(df_inm)

   print(df_inmlb.head(2))

   # Análisis de CSV de Ñuñoa
   df_inm = pd.read_csv("EDA_Inmob_Nunoa.csv")

   df_inmnu = editar_csv(df_inm)

   print(df_inmnu.head(2))

    # Análisis de CSV de Las Condes
   df_inm = pd.read_csv("EDA_Inmob_Lascondes.csv")

   df_inmlc = editar_csv(df_inm)

   print(df_inmlc.head(2))

   # Agrupo por m2 y hago una tabla describe estadística
   # Etiquetas = ['<40', '40-60', '60-80', '80-100','100-120','>120']
   desc_nu  = desc_gruposm2(df_inmnu)
   print(desc_nu)
   desc_lb  = desc_gruposm2(df_inmlb)
   print(desc_lb)
   desc_lc  = desc_gruposm2(df_inmlc)
   print(desc_lc)

# Agrupo en una misma tabla para mostrar
   desc_total = pd.concat([desc_nu[["mean", "50%"]], desc_lc[["mean", "50%"]], desc_lb[["mean", "50%"]]],
   axis=1,keys=["Ñuñoa", "Las Condes", "Lo Barnechea"])
   print(desc_total)


# Para las características específicas de mi búsqueda filtro el df de Nunoa
#df_inmnu2 = filtrar_busqueda(df_inmnu,dorm,estac,m2_min,m2_max):
   
   df_inmnu2 = filtrar_busqueda(df_inmnu,2,1,60,80)
   print(df_inmnu2.describe())


if __name__ == "__main__":
    main()