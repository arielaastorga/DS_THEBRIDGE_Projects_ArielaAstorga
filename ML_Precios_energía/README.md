# Electricity Price Forecasting for Energy Storage Optimization

### Overview
This project develops machine learning models to forecast hourly marginal electricity prices using meteorological, radiation, and temporal variables. The use case is linked to a private company, to create an energy storage application that benefits from identifying low-price periods for electricity purchase and storage.[1][2]

The work focuses on the Crucero substation in the Atacama Region of Chile and uses 2024 hourly marginal price data combined with weather-related variables. The final modeling dataset includes 14 predictive variables and was built by integrating electricity price records with meteorological information through common time fields such as month, day, and hour.[1]

### Objective
The main objective is to estimate hourly electricity prices in order to support decision-making for energy storage operation. In practical terms, the project seeks to detect the periods of the day when electricity prices are low or even near zero, which is especially relevant in systems with strong solar generation penetration.[1]

### Data Sources
The project combines two main data sources:

- Hourly marginal electricity prices for the Crucero node/bar in Chile during 2024.[1]
- Meteorological and radiation variables aligned by time fields.[1]

The notebooks indicate that the price dataset includes date, year, month, day, hour, node/substation, voltage, and electricity value, although voltage was not considered relevant for prediction. The integrated dataset used for modeling includes temporal variables, atmospheric variables, and radiation indicators such as DNI and GHI.[1]

### Methodology
The methodological workflow was structured into three main stages:[1]

1. Data integration from different monthly and meteorological sources into a unified dataset.[1]
2. Data cleaning and exploratory analysis to understand distributions and patterns in the predictors.[1]
3. Predictive modeling using supervised and unsupervised learning techniques.[1][2]

For supervised learning, the project evaluated Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting, and XGBoost. The modeling workflow also included train-test split, preprocessing pipelines, hyperparameter tuning with GridSearchCV, and 5-fold cross-validation.[1]

For unsupervised learning, KMeans was used to detect representative behavioral profiles, and PCA was applied to improve visualization and interpretation of the clusters. 
KMeans was also used to build representative hourly price curves for each month after restructuring the dataset so that each row represented one day and the 24 hourly prices became columns.[1]

### Results
The notebooks report that linear models such as Linear Regression, Ridge, and Lasso achieved R2 values around 0.66, with RMSE values around 28.8 to 28.9, indicating moderate predictive performance. Nonlinear methods performed better, with Random Forest reaching an R2 of 0.88, Gradient Boosting around 0.80, and XGBoost around 0.83 in the narrative results section.[1]

The same notebook also includes a later output stating that the selected final model was XGBoost with MinMaxScaler, with an R2 of 
0.88 and the best overall performance among the tested alternatives. Because the notebook contains both statements, the most accurate interpretation is that the project identified top performance at R2 = 0.88, while the final selected model in the latest reported output was XGBoost with MinMaxScaler.[1]

The reported best-performing configuration used the 14-variable dataset and a reduced sample of 5,000 observations, while alternative setups with fewer variables or the full dataset performed worse.[1]

### Repository Structure
The structure for this repository is:

Proyecto ML _energíaR/
├── data/
│   ├── processed
│   ├── raw
│   ├── train
│   └── test
├── docs/
│   ├── memoria
│   └── Negocio y DS.pptx
├── img/
├── models/
│   └──finalmodel.pkl
├── notebooks/
│   ├── 01_Fuentes-3.ipynb
│   ├── 02_LimpiezaEDA-4.ipynb
│   ├── 03_Entrenamiento_Evaluacion-2.ipynb
│   ├── raw
│   ├── train
│   └── test
├── src/
│   ├── data_processing.py
│   ├── evaluation.py
│   ├── modelo_pipe.pkl
│   └── training.py
└── README.md


### Tools and Techniques
- Python and Jupyter Notebook for analysis and experimentation.[1][2]
- Scikit-learn pipelines and GridSearchCV for model development and tuning.[1]
- PCA and KMeans for unsupervised pattern discovery.[1]
- Regression-based ensemble methods for nonlinear forecasting.[1]

### Applications
This project is relevant for:

- Energy storage dispatch optimization.[1]
- Electricity market forecasting.[1]
- Renewable-energy-aware operational planning, especially in systems with strong solar influence.[1]





### Descripción general
Este proyecto desarrolla modelos de aprendizaje automático para pronosticar el precio marginal horario de la electricidad utilizando variables meteorológicas, de radiación y temporales. El caso de uso está vinculado a **Thermophoton**, una aplicación de almacenamiento energético que se beneficia de identificar los periodos de bajo precio para comprar y almacenar electricidad.[1][2]

El trabajo se centra en la subestación Crucero, en la Región de Atacama, Chile, y utiliza datos horarios de precios marginales de 2024 combinados con variables meteorológicas. El conjunto final de modelado contiene 14 variables predictoras y fue construido integrando registros de precio eléctrico con información meteorológica mediante variables temporales comunes como mes, día y hora.[1]

### Objetivo
El objetivo principal es estimar precios eléctricos horarios para apoyar la toma de decisiones en la operación de sistemas de almacenamiento de energía. En términos prácticos, el proyecto busca detectar los momentos del día en que el precio de la electricidad es bajo o incluso cercano a cero, algo especialmente relevante en sistemas con alta penetración de generación solar.[1]

### Fuentes de datos
El proyecto combina dos fuentes principales de datos:

- Precios marginales horarios de electricidad para la barra/subestación Crucero en Chile durante 2024.[1]
- Variables meteorológicas y de radiación alineadas mediante campos temporales.[1]

Los notebooks indican que el dataset de precios incluye fecha, año, mes, día, hora, barra/subestación, tensión y valor de la electricidad, aunque la tensión no fue considerada relevante para la predicción. El dataset integrado utilizado para el modelado incluye variables temporales, variables atmosféricas e indicadores de radiación como DNI y GHI.[1]

### Metodología
El flujo metodológico se estructuró en tres etapas principales:[1]

1. Integración de datos desde distintas fuentes mensuales y meteorológicas en un único dataset.[1]
2. Limpieza de datos y análisis exploratorio para comprender distribuciones y patrones en las variables predictoras.[1]
3. Modelado predictivo mediante técnicas supervisadas y no supervisadas.[1][2]

En aprendizaje supervisado se evaluaron Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting y XGBoost. Además, el flujo de trabajo incluyó train-test split, pipelines de preprocesamiento, ajuste de hiperparámetros con GridSearchCV y validación cruzada de 5 folds.[1]

En aprendizaje no supervisado se utilizó KMeans para detectar perfiles representativos de comportamiento y PCA para mejorar la visualización e interpretación de los clústeres. KMeans también se utilizó para construir curvas representativas del precio horario por mes después de reestructurar el dataset para que cada fila representara un día y las 24 horas fueran columnas.[1]

### Resultados
Los notebooks reportan que los modelos lineales, como Linear Regression, Ridge y Lasso, alcanzaron valores de R2 cercanos a 0.66, con RMSE entre 28.8 y 28.9, lo que indica una capacidad predictiva moderada. Los métodos no lineales mostraron un mejor desempeño, con Random Forest alcanzando un R2 de 0.88, Gradient Boosting alrededor de 0.80 y XGBoost alrededor de 0.83 en la sección narrativa de resultados.[1]

El mismo notebook también incluye una salida posterior donde se afirma que el modelo final seleccionado fue XGBoost con MinMaxScaler, con un R2 de 0.88 y el mejor desempeño general entre las alternativas probadas. Como el notebook contiene ambas afirmaciones, la interpretación más precisa es que el mejor desempeño reportado fue R2 = 0.88 y que el modelo final seleccionado en la última salida reportada fue XGBoost con MinMaxScaler.[1]

La configuración de mejor desempeño reportada utilizó el dataset con 14 variables y una muestra reducida de 5.000 observaciones, mientras que configuraciones alternativas con menos variables o con el dataset completo tuvieron peores resultados.[1]

### Estructura del repositorio
Estructura para este repositorio:

Proyecto ML _energíaR/
├── data/
│   ├── processed
│   ├── raw
│   ├── train
│   └── test
├── docs/
│   ├── memoria
│   └── Negocio y DS.pptx
├── img/
├── models/
│   └──finalmodel.pkl
├── notebooks/
│   ├── 01_Fuentes-3.ipynb
│   ├── 02_LimpiezaEDA-4.ipynb
│   ├── 03_Entrenamiento_Evaluacion-2.ipynb
│   ├── raw
│   ├── train
│   └── test
├── src/
│   ├── data_processing.py
│   ├── evaluation.py
│   ├── modelo_pipe.pkl
│   └── training.py
└── README.md



### Herramientas y técnicas
- Python y Jupyter Notebook para análisis y experimentación.[1][2]
- Pipelines de Scikit-learn y GridSearchCV para desarrollo y ajuste de modelos.[1]
- PCA y KMeans para descubrimiento de patrones no supervisados.[1]
- Métodos de ensamble de regresión para capturar relaciones no lineales.[1]

### Aplicaciones
Este proyecto es relevante para:

- Optimización de operación de sistemas de almacenamiento de energía.[1]
- Pronóstico de precios en mercados eléctricos.[1]
- Planificación operativa sensible a renovables, especialmente en sistemas con fuerte influencia solar.[1]