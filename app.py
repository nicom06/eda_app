'''Aplicación en Streamlit para Analisis Exploratorio de Datos (EDA)'''

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

#Imnportar módulos personalizados 
from data_processor import DataProcessor
from visualizations import DataVisualizations
from utils import (
    load_dataset, validate_dataframe, get_column_types,
    format_number, format_percentage
)

## CONFIGURACIÓN DE PÁGINA

def setup_page():
    st.set_page_config(
        page_title="Data Analytics Explorer",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
### INICIALIZAR SESIÓN

def initialize_session():
    """Inicializa variables de sesión de Streamlit"""
    if 'df' not in st.session_state:
        st.session_state.df=None
    if 'processor' not in st.session_state:
        st.session_state.df=None
    if 'loaded' not in st.session_state:
        st.session_state.loaded=False

### SIDEBAR - CARGA DE DATOS

def render_sidebar():
    """Renderiza la barra lateral con la opcion de carga"""
    with st.sidebar:
        st.markdown("Data Analytics Explorer")
        st.markdown("---")

        st.markdown("## Control de Datos")

        #Selector de fuente
        data_source=st.radio(
            "Selecciona la fuente de datos:",
            ["Cargar archivo","Dataset de ejemplo"],
            label_visibility="collapsed",
            key="data_source"
        )

        #Opcion 1: Cargar archivo
        if data_source == "Cargar archivo":
            st.markdown("### Sube tu archivo CSV o Excel")

            uploaded_file=st.file_uploader(
                "Selecciona un archivo",
                type=['csv','xlsx','xls'],
                help="Formatos soportados: CSV, XLSX, XLS",
                label_visibility="collapsed"
            )

            if uploaded_file is not None:
                try:
                    with st.spinner("Cargando archivo..."):
                        df=load_dataset(uploaded_file)
                        validate_dataframe(df)
                        st.session_state.df=df
                        st.session_state.processor=DataProcessor(df)
                        st.session_state.loaded=True
                        st.success("Dataset cargado exitosamente")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        #Opcion 2: Dataset ejemplo "BankMarketing"
        else:
            st.markdown("### Dataset de ejemplo")

            if st.button("Bank Marketing", use_container_width=True,key="load_bank"):
                try:
                    with st.spinner("Descargando dataset..."):
                        df = load_dataset('bank_marketing')
                        validate_dataframe(df)
                        st.session_state.df = df
                        st.session_state.processor = DataProcessor(df)
                        st.session_state.loaded = True
                        st.success("Dataset cargado")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        st.markdown("---")

        #### 1. Información del dataset cargado
        if st.session_state.loaded and st.session_state.df is not None:
            df=st.session_state.df

            st.markdown("### Información Rápida")

            col1, col2 =st.columns(2)
            with col1:
                st.metric("filas",f"{df.shape[0]:,}") 
            with col2:
                st.metric("Columnas",f"{df.shape[1]:,}")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            categorical_cols=df.select_dtypes(include=['object']).columns.tolist()

            if len(numeric_cols) > 0:
                st.info(f"Numericas: {len(numeric_cols)}")
            if categorical_cols:
                st.info(f"Categoricas: {len(categorical_cols)}")

            missing_pct=(df.isnull().sum().sum() / (df.shape[0]*df.shape[1]))
            if missing_pct > 0:
                st.warning(f"Faltantes: {missing_pct:.2f}%")
            else:
                st.success("Sin Faltantes")

            st.markdown("---")

            if st.button("Limpiar datos",use_container_width=True):
                st.session_state.df=None
                st.session_state.processor=None
                st.session_state.loaded=False
                st.rerun()

        st.markdown("---")

### PÁGINA DE INICIO

def show_home_page():
    st.markdown("""
    ## Data Analytics Explorer
    ## Análisis Exploratorio de Datos Interactivo
    
    Bienvenido a tu herramienta profesional de análisis de datos.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Estadísticas
        - Media, mediana, desv. est.
        - Cuartiles y percentiles
        """)
    
    with col2:
        st.markdown("""
        ### Visualizaciones
        - Histogramas
        - Scatter plots
        """)
    
    with col3:
        st.markdown("""
        ### Análisis
        - Correlaciones
        - Outliers
        """)
    
    st.markdown("---")
    st.markdown("""
    ## ¿Cómo Comenzar?
    
    1. Carga un archivo en la barra lateral
    2. O usa el dataset "Bank Marketing" de ejemplo
    3. Explora los análisis en las pestañas
    """)

# ============================================================================
# FUNCIONES DE LOS 10 ÍTEMS
# ============================================================================

def show_item1_general_info(processor):
    """ÍTEM 1: Información General"""
    st.markdown("## Información General del Dataset")
    
    df = processor.df
    info = processor.get_general_info()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Filas", f"{info['filas']:,}")
    with col2:
        st.metric("Columnas", f"{info['columnas']:,}")
    with col4:
        st.metric("Faltantes", f"{info['porcentaje_nulos']:.2f}%")
    
    st.markdown("---")
    
    st.markdown("### Tipos de Datos")
    dtypes_summary = processor.get_data_types_summary()
    st.dataframe(dtypes_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### Primeras Filas")
    st.dataframe(df.head(10), use_container_width=True)

def show_item2_variable_classification(processor):
    """ÍTEM 2: Clasificación de Variables"""
    st.markdown("## Clasificación de Variables")
    
    col_types = processor.classify_variables()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Numéricas", len(col_types['numeric']))
    with col2:
        st.metric("Categóricas", len(col_types['categorical']))
    with col3:
        st.metric("Datetime", len(col_types['datetime']))
    with col4:
        st.metric("Booleanas", len(col_types['boolean']))
    
    st.markdown("---")
    
    st.markdown("### Tabla de Variables")
    vars_summary = processor.get_variables_summary()
    st.dataframe(vars_summary, use_container_width=True, hide_index=True)


def show_item3_descriptive_stats(processor):
    """ÍTEM 3: Estadísticas Descriptivas"""
    st.markdown("## Estadísticas Descriptivas")
    
    st.markdown("### Tabla de Estadísticas")
    stats_df = processor.get_descriptive_statistics()
    st.dataframe(stats_df, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Análisis Detallado")
    numeric_stats = processor.get_numeric_statistics()
    st.dataframe(numeric_stats, use_container_width=True)


def show_item4_missing_values(processor):
    """ÍTEM 4: Análisis de Valores Faltantes"""
    st.markdown("## Valores Faltantes")
    
    missing_pct = processor.get_missing_percentage()
    has_missing = processor.has_missing_values()
    
    if not has_missing:
        st.success("No hay valores faltantes en el dataset")
        return
    
    st.warning(f"⚠️ {missing_pct:.2f}% de valores faltantes")
    
    st.markdown("---")
    
    st.markdown("### Conteo")
    missing_summary = processor.get_missing_values_summary()
    st.dataframe(missing_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### Visualización")
    viz = DataVisualizations(processor.df)
    fig_missing = viz.create_missing_values_bar()
    st.plotly_chart(fig_missing, use_container_width=True)


def show_item5_numeric_distributions(processor):
    """ÍTEM 5: Distribuciones Numéricas"""
    st.markdown("## Distribuciones de Variables Numéricas")
    
    numeric_cols = processor.column_types['numeric']
    
    if not numeric_cols:
        st.info("No hay variables numéricas")
        return
    
    selected_col = st.selectbox("Selecciona variable:", numeric_cols, key="num_dist")
    
    st.markdown("---")
    
    viz = DataVisualizations(processor.df)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_hist = viz.create_histogram(selected_col)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.markdown("### Info")
        data = processor.df[selected_col].dropna()
        st.metric("Media", f"{data.mean():.2f}")
        st.metric("Mediana", f"{data.median():.2f}")
        st.metric("Desv. Est.", f"{data.std():.2f}")


def show_item6_categorical_analysis(processor):
    """ÍTEM 6: Variables Categóricas"""
    st.markdown("## Variables Categóricas")
    
    categorical_cols = processor.column_types['categorical']
    
    if not categorical_cols:
        st.info("No hay variables categóricas")
        return
    
    selected_col = st.selectbox("Selecciona variable:", categorical_cols, key="cat_var")
    
    st.markdown("---")
    
    viz = DataVisualizations(processor.df)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_bar = viz.create_bar_chart(selected_col)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("### Tabla")
        summary = processor.get_categorical_summary(selected_col)
        st.dataframe(summary, use_container_width=True, hide_index=True)


def show_item7_bivariate_num_cat(processor):
    """ÍTEM 7: Bivariado Numérico-Categórico"""
    st.markdown("## Análisis: Numérico vs Categórico")
    
    numeric_cols = processor.column_types['numeric']
    categorical_cols = processor.column_types['categorical']
    
    if not numeric_cols or not categorical_cols:
        st.info("Se requieren variables numéricas y categóricas")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        num_col = st.selectbox("Numérica:", numeric_cols, key="num_biv")
    with col2:
        cat_col = st.selectbox("Categórica:", categorical_cols, key="cat_biv")
    
    st.markdown("---")
    
    grouped = processor.get_numeric_by_category(num_col, cat_col)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        viz = DataVisualizations(processor.df)
        fig_box = viz.create_categorical_boxplot(cat_col, num_col)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        st.markdown("### Estadísticas")
        st.dataframe(grouped, use_container_width=True)


def show_item8_bivariate_cat_cat(processor):
    """ÍTEM 8: Bivariado Categórico-Categórico"""
    st.markdown("## Análisis: Categórico vs Categórico")
    
    categorical_cols = processor.column_types['categorical']
    
    if len(categorical_cols) < 2:
        st.info("Se requieren 2 variables categóricas")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        cat1 = st.selectbox("Primera:", categorical_cols, key="cat_biv1")
    with col2:
        cat2 = st.selectbox(
            "Segunda:",
            [c for c in categorical_cols if c != cat1],
            key="cat_biv2"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        viz = DataVisualizations(processor.df)
        fig_heat = viz.create_heatmap_crosstab(cat1, cat2)
        st.plotly_chart(fig_heat, use_container_width=True)
    
    with col2:
        crosstab = processor.get_categorical_crosstab(cat1, cat2)
        st.markdown("### Tabla")
        st.dataframe(crosstab, use_container_width=True)


def show_item9_dynamic_analysis(processor):
    """ÍTEM 9: Análisis Dinámico"""
    st.markdown("## Análisis Dinámico Personalizado")
    
    st.markdown("### Análisis de una Variable")
    
    selected_col = st.selectbox("Selecciona:", processor.df.columns, key="dynamic_col")
    
    col_stats = processor.get_column_statistics(selected_col)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tipo", col_stats['tipo'])
    with col2:
        st.metric("Únicos", col_stats['unicos'])
    with col3:
        st.metric("Nulos", col_stats['nulos'])
    
    if 'media' in col_stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Media", f"{col_stats['media']:.2f}")
        with col2:
            st.metric("Mediana", f"{col_stats['mediana']:.2f}")
        with col3:
            st.metric("Desv. Est.", f"{col_stats['desv_est']:.2f}")
    
    st.markdown("---")
    
    st.markdown("### Comparar Múltiples Variables")
    
    all_cols = processor.df.columns.tolist()
    selected_cols = st.multiselect(
        "Variables:",
        options=all_cols,
        default=all_cols[:3] if len(all_cols) >= 3 else all_cols,
        key="multi_cols"
    )
    
    if selected_cols:
        comparison_data = []
        for col in selected_cols:
            comparison_data.append(processor.get_column_statistics(col))
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)


def show_item10_key_findings(processor):
    """ÍTEM 10: Hallazgos Clave"""
    st.markdown("## Hallazgos Clave e Insights")
    
    findings = processor.get_key_findings()
    
    for i, (key, finding) in enumerate(findings.items(), 1):
        st.markdown(f"### Hallazgo {i}")
        st.info(finding)
    
    st.markdown("---")
    
    st.markdown("### Correlaciones Principales")
    
    corr_matrix = processor.get_correlation_matrix()
    
    if not corr_matrix.empty:
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    corr_pairs.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlación': f"{corr_val:.3f}"
                    })
        
        if corr_pairs:
            corr_df = pd.DataFrame(corr_pairs)
            st.dataframe(corr_df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay correlaciones significativas (> 0.5)")


def show_correlation_matrix(processor):
    """Muestra matriz de correlaciones completa"""
    st.markdown("## Matriz de Correlaciones")
    
    numeric_cols = processor.column_types['numeric']
    
    if not numeric_cols:
        st.info("No hay variables numéricas")
        return
    
    corr_matrix = processor.get_correlation_matrix()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        viz = DataVisualizations(processor.df)
        fig_corr = viz.create_correlation_heatmap(corr_matrix)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.markdown("### Matriz")
        st.dataframe(corr_matrix, use_container_width=True)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal."""
    
    setup_page()
    initialize_session()
    render_sidebar()
    
    if not st.session_state.loaded:
        show_home_page()
    else:
        # Crear tabs para los 10 ítems + 1 extra
        tabs = st.tabs([
            "General",
            "Variables",
            "Estadísticas",
            "Nulos",
            "Numéricos",
            "Categóricos",
            "Num-Cat",
            "Cat-Cat",
            "Dinámico",
            "Correlaciones",
            "Hallazgos"
        ])
        
        processor = st.session_state.processor
        
        with tabs[0]:
            show_item1_general_info(processor)
        
        with tabs[1]:
            show_item2_variable_classification(processor)
        
        with tabs[2]:
            show_item3_descriptive_stats(processor)
        
        with tabs[3]:
            show_item4_missing_values(processor)
        
        with tabs[4]:
            show_item5_numeric_distributions(processor)
        
        with tabs[5]:
            show_item6_categorical_analysis(processor)
        
        with tabs[6]:
            show_item7_bivariate_num_cat(processor)
        
        with tabs[7]:
            show_item8_bivariate_cat_cat(processor)
        
        with tabs[8]:
            show_item9_dynamic_analysis(processor)
        
        with tabs[9]:
            show_correlation_matrix(processor)
        
        with tabs[10]:
            show_item10_key_findings(processor)


if __name__ == "__main__":
    main()
