# Análisis inmobiliario Ariela

Proyecto de análisis exploratorio de datos (EDA) sobre el mercado de alquiler residencial en dos mercados geográficos: Santiago de Chile y Madrid. El objetivo es comparar precios, superficie y patrones de mercado mediante web scraping, limpieza de datos y análisis estadístico.

## Descripción del proyecto

Este proyecto estudia el comportamiento del alquiler residencial en:

- Chile: Ñuñoa, Las Condes y Lo Barnechea.
- España: zona norte de Madrid, cercana a Tetúan.

El análisis busca responder preguntas como:

- ¿Cómo se distribuyen los precios entre comunas y barrios? 
- ¿Qué relación existe entre precio y superficie?
- ¿Cómo cambia el precio por metro cuadrado según el tamaño del inmueble?
- ¿Existen diferencias estadísticamente significativas entre zonas?

## Fuentes de datos

### Chile
Se recolectaron datos desde `chilepropiedades.cl` usando Selenium con `undetected-chromedriver`. Los campos extraídos por propiedad incluyen título, precio mensual en CLP, dormitorios, baños, metros cuadrados, código, estacionamientos y fecha de publicación.

El dataset de Chile contiene 666 registros en total, distribuidos así:

- Ñuñoa: 353 pisos.
- Las Condes: 265 pisos.
- Lo Barnechea: 48 pisos.

### Madrid
Para Madrid se realizó web scraping en Idealista usando búsqueda por área geográfica, en el distrito de Tetuán ampliado a zonas colindantes. Se extrajeron 695 propiedades en 24 páginas, con campos como título, precio mensual, habitaciones, superficie, planta y ubicación inferida por regex.

### Referencias de contexto
Se utilizó Expatistan como referencia para comparar coste de vida entre Madrid y Santiago, donde el promedio de Madrid aparece como 49% más caro que Santiago.

## Metodología

El flujo de trabajo del proyecto incluye:

1. Web scraping de portales inmobiliarios.
2. Limpieza y normalización de datos.
3. Conversión de precios a euros.
4. Cálculo de precio por metro cuadrado.
5. Eliminación de outliers mediante percentiles.
6. Análisis descriptivo, bivariante y comparativo.
7. Pruebas estadísticas, incluyendo ANOVA.

## Procesamiento de datos

En la limpieza se realizaron tareas como:

- Conversión de precios a formato numérico.
- Conversión de superficie a formato numérico.
- Transformación de precios de CLP a EUR con tipo de cambio fijo de 1 CLP = 0.00094 EUR.
- Cálculo de `precio_eur_m2`.
- Eliminación de valores nulos.
- Reemplazo de `NaN` en estacionamientos por 0.
- Limpieza de texto redundante en títulos y códigos.

También se aplicó un filtro de outliers usando percentiles p5 y p95 sobre el precio en euros o el precio por metro cuadrado, eliminando aproximadamente el 10% de los valores extremos.

## Stack tecnológico

### Web scraping
- Selenium.
- `undetected-chromedriver`.
- `webdriver_manager`.
- `numpy`.
- EC waits / esperas explícitas.

### Análisis y visualización
- `pandas` para limpieza y agrupación.
- `seaborn` y `matplotlib` para gráficos.
- Funciones personalizadas para visualizaciones.
- Pruebas estadísticas con ANOVA.

## Estructura del análisis

El notebook incluye análisis por distrito y comparaciones entre zonas:

- Análisis univariante de precios.
- Análisis bivariante precio vs. m².
- Relación entre precio y número de baños.
- Segmentación por tramos de superficie.
- Comparación entre comunas de Santiago.
- Comparación entre Santiago y Madrid para un perfil comparable.

## Hallazgos principales

### Santiago de Chile
- El precio por m² varía significativamente entre comunas, con ANOVA F = 62.21 y p < 0.001.
- Las Condes y Lo Barnechea tienen mayor precio por m² que Ñuñoa en mediana.
- El precio total sí muestra correlación positiva con la superficie.
- El precio por m² muestra correlación negativa con la superficie: a más metros, menor precio unitario.
- Los outliers son frecuentes, especialmente en Las Condes y Ñuñoa.

### Madrid
- La zona norte de Madrid analizada muestra precios típicos entre 800 y 2.000 euros/mes.
- El patrón general de precios es consistente con una mayor presión de coste que en Santiago.

### Comparación Madrid vs. Santiago
- Para pisos de 60–80 m² con 2 habitaciones, la mediana de alquiler en Ñuñoa es aproximadamente 48% menor que en Tetúan.
- En el análisis de coste de vida, Madrid resulta más caro en vivienda y, por tanto, más exigente para el presupuesto mensual.
- En Santiago, el mayor gasto en salud privada compensa parcialmente la diferencia, pero la capacidad de ahorro sigue siendo más favorable.

## Notas técnicas

- El archivo `utils` incluye funciones para leer, editar y transformar CSV, con el objetivo de hacer el estudio escalable a otros ayuntamientos.
- El tipo de cambio usado es fijo y corresponde a abril de 2026.
- Los scripts de scraping son reutilizables cambiando la URL y el número de páginas.
- Se usa `undetected-chromedriver` compatible con Chrome 146.

## Requisitos

Dependencias recomendadas:

- Python 3.11.
- pandas.
- numpy.
- matplotlib.
- seaborn.
- selenium.
- undetected-chromedriver.
- webdriver-manager.

## Uso

1. Ejecuta el notebook principal.
2. Verifica que los datos de scraping estén disponibles.
3. Corre las celdas de limpieza y análisis.
4. Revisa los gráficos y tablas generadas.
5. Consulta las conclusiones finales del notebook.

## Autoría

Proyecto elaborado por Ariela Astorga.