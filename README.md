# Data Analytics Explorer - EDA con Streamlit

## Descripción del Proyecto

Aplicación interactiva desarrollada en **Streamlit** para realizar **Análisis Exploratorio de Datos (EDA)** completo sobre cualquier dataset. La aplicación implementa los conceptos fundamentales de Python incluyendo POO, Pandas, NumPy y visualizaciones profesionales.

**Características principales:**
- Carga flexible de datasets (CSV, Excel, URL)
- **10 ítems de análisis mínimo** como se requiere
- Interfaz profesional con tabs, columnas y sidebar
- Visualizaciones interactivas con Plotly
- Clase POO `DataProcessor` que encapsula toda la lógica
- Estadísticas descriptivas completas
- Análisis bivariado y correlaciones
- Hallazgos automáticos e insights

---

## Los 10 Ítems de Análisis Implementados

| # | Ítem | Descripción |
|---|------|------------|
| 1 | **Información General** | Dimensiones, tipos de datos, valores nulos |
| 2 | **Clasificación de Variables** | Separación en numéricas, categóricas, datetime |
| 3 | **Estadísticas Descriptivas** | Media, mediana, desv. est., cuartiles |
| 4 | **Análisis de Nulos** | Conteo y visualización de faltantes |
| 5 | **Distribuciones Numéricas** | Histogramas, violin plots |
| 6 | **Variables Categóricas** | Conteos, gráficos de barras, pastel |
| 7 | **Bivariado Numérico-Categórico** | Boxplots por grupo |
| 8 | **Bivariado Categórico-Categórico** | Tablas de contingencia, heatmaps |
| 9 | **Análisis Dinámico** | Exploración personalizada con selectbox/multiselect |
| 10 | **Hallazgos Clave** | Insights automáticos e interpretaciones |

---

## Estructura del Proyecto

```
eda_app/
├── app.py              # Aplicación Streamlit principal
├── data_processor.py            # Clase POO para análisis
├── visualizations.py            # Funciones de visualización
├── utils.py                     # Funciones auxiliares
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
├── data/
    └── bank_marketing.csv       # Dataset 
```

## Cómo Usar la Aplicación

### Paso 1: Cargar Datos
1. Abre la aplicación: `streamlit run app_completa.py`
2. En el **sidebar izquierdo**, elige:
   - **Opción A:** Carga tu archivo CSV/Excel
   - **Opción B:** USA el dataset "Bank Marketing" de ejemplo

### Paso 2: Explorar los Análisis
Navega por las **11 pestañas** (tabs) para explorar:
- Información General
- Clasificación de Variables
- Estadísticas Descriptivas
- Valores Faltantes
- Distribuciones Numéricas
- Variables Categóricas
- Análisis Bivariado (Numérico-Categórico)
- Análisis Bivariado (Categórico-Categórico)
- Análisis Dinámico (personalizado)
- Matriz de Correlaciones
- Hallazgos Clave

### Paso 3: Interactuar
- Usa **selectbox** para elegir variables
- **Multiselect** para comparar múltiples variables
- Consulta **gráficos interactivos** (zoom, pan, etc.)
- Lee las **interpretaciones automáticas**

--

## Dataset Bank Marketing

La aplicación incluye el dataset "Bank Marketing" correspondiente a una institución 
financiera que busca entender los factores que influyen en la aceptación de sus 
campañas de marketing. 
Durante los últimos 6 meses, la efectividad (e = (Ventas/Base)×100%) cayó de 12% 
a 8%, afectando los bonos de los ejecutivos comerciales. 

**Columnas principales:**
- `age`: Edad del cliente
- `job`: Ocupación
- `marital`: Estado Civil
- `education`: Nivel Educativo
- `default`: ¿Tiene crédito en mora?
- `housing`: ¿Tiene crédito hipotecario?
- `loan`: ¿Tiene crédito personal?
- `contact`: Canal de comunicacion usado

---

## Contacto y Créditos

**Desarrollado como:** Proyecto Final - Curso Python para Analytics - DMC 2026

**Tecnologías utilizadas:**
- Python 3.8+
- Streamlit
- Pandas & NumPy
- Matplotlib & Seaborn
- Plotly

**Licencia:** MIT (código abierto)

---

**¡Gracias por usar Data Analytics Explorer!**

*Última actualización: Mayo 2026*
