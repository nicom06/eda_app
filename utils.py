"""
utils.py - Funciones auxiliares para la aplicación

Este módulo contiene funciones de utilidad para:
- Cargar datos de diferentes formatos
- Validar dataframes
- Formatear información para mostrar
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
import io


def load_dataset(source):
    """
    Carga un dataset desde diferentes fuentes.
    
    Args:
        source: Puede ser:
            - Un objeto de archivo subido (UploadedFile de Streamlit)
            - Una cadena con el nombre del dataset de ejemplo ('bank_marketing')
            - Una ruta a un archivo local
    
    Returns:
        DataFrame de pandas
        
    Raises:
        ValueError: Si el archivo no puede cargarse o no es válido
        FileNotFoundError: Si el archivo no existe
    
    Ejemplos:
        >>> df = load_dataset(uploaded_file)  # Archivo subido
        >>> df = load_dataset('bank_marketing')  # Dataset de ejemplo
    """
    
    # Caso 1: Archivo subido a través de Streamlit
    if hasattr(source, 'name'):
        file_extension = source.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'csv':
                df = pd.read_csv(source)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(source)
            else:
                raise ValueError(f"❌ Formato no soportado: {file_extension}")
            
            return df
            
        except Exception as e:
            raise ValueError(f"❌ Error al leer archivo: {str(e)}")
    
    # Caso 2: Dataset de ejemplo 'bank_marketing'
    elif isinstance(source, str) and source.lower() == 'bank_marketing':
        try:
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, 'BankMarketing.csv')
            df = pd.read_csv(csv_path, sep=';')
            return df
        except Exception as e:
            raise ValueError(f"❌ No se pudo cargar el dataset: {str(e)}")
    
    # Caso 3: Ruta local
    elif isinstance(source, str):
        file_path = Path(source)
        
        if not file_path.exists():
            raise FileNotFoundError(f"❌ Archivo no encontrado: {source}")
        
        try:
            if source.endswith('.csv'):
                df = pd.read_csv(source)
            elif source.endswith('.xlsx') or source.endswith('.xls'):
                df = pd.read_excel(source)
            else:
                raise ValueError(f"❌ Formato no soportado")
            return df
        except Exception as e:
            raise ValueError(f"❌ Error al cargar archivo local: {str(e)}")
    
    else:
        raise ValueError("❌ Tipo de fuente no reconocido")


def validate_dataframe(df):
    """
    Valida que el dataframe sea válido para análisis.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        
    Raises:
        ValueError: Si el dataframe no es válido
        
    Verifica:
        - No está vacío
        - Tiene al menos 2 filas y 1 columna
        - No es None
    """
    
    if df is None:
        raise ValueError("❌ El dataframe es None")
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError("❌ El objeto no es un DataFrame válido")
    
    if df.empty:
        raise ValueError("❌ El dataframe está vacío")
    
    if df.shape[0] < 2:
        raise ValueError("❌ El dataframe debe tener al menos 2 filas")
    
    if df.shape[1] < 1:
        raise ValueError("❌ El dataframe debe tener al menos 1 columna")


def get_column_types(df):
    """
    Clasifica las columnas del dataframe en tipos.
    
    Args:
        df (pd.DataFrame): Dataframe a analizar
        
    Returns:
        dict: Diccionario con listas de columnas por tipo
        
    Ejemplo:
        >>> types = get_column_types(df)
        >>> print(types['numeric'])
        ['age', 'balance', 'duration']
    """
    
    column_types = {
        'numeric': [],      # int64, float64
        'categorical': [],  # object, category
        'datetime': [],     # datetime64
        'boolean': []       # bool
    }
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types['numeric'].append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            column_types['datetime'].append(col)
        elif pd.api.types.is_bool_dtype(df[col]):
            column_types['boolean'].append(col)
        else:  # object, category
            column_types['categorical'].append(col)
    
    return column_types


def format_number(value, decimals=2):
    """
    Formatea un número para presentación.
    
    Args:
        value (float): Número a formatear
        decimals (int): Decimales a mostrar (default: 2)
        
    Returns:
        str: Número formateado
        
    Ejemplo:
        >>> format_number(1234.5678)
        '1,234.57'
    """
    
    if pd.isna(value):
        return "N/A"
    
    try:
        return f"{value:,.{decimals}f}"
    except:
        return str(value)


def format_percentage(value, decimals=2):
    """
    Formatea un valor como porcentaje.
    
    Args:
        value (float): Valor entre 0 y 1
        decimals (int): Decimales a mostrar (default: 2)
        
    Returns:
        str: Porcentaje formateado
        
    Ejemplo:
        >>> format_percentage(0.456)
        '45.60%'
    """
    
    if pd.isna(value):
        return "N/A"
    
    return f"{value * 100:.{decimals}f}%"


def create_summary_stats(series):
    """
    Crea un diccionario con estadísticas resumidas de una serie.
    
    Args:
        series (pd.Series): Serie a analizar
        
    Returns:
        dict: Diccionario con estadísticas
        
    Utiliza:
        - NumPy para cálculos estadísticos
        - Pandas para métodos de Series
    """
    
    if series.dtype in ['float64', 'int64']:
        # Variable numérica
        return {
            'Tipo': 'Numérica',
            'Conteo': len(series),
            'Media': series.mean(),
            'Mediana': series.median(),
            'Desv. Est.': series.std(),
            'Mínimo': series.min(),
            'Máximo': series.max(),
            'Q1': series.quantile(0.25),
            'Q3': series.quantile(0.75),
            'Nulos': series.isnull().sum(),
            'Únicos': series.nunique()
        }
    else:
        # Variable categórica
        return {
            'Tipo': 'Categórica',
            'Conteo': len(series),
            'Únicos': series.nunique(),
            'Moda': series.mode()[0] if len(series.mode()) > 0 else 'N/A',
            'Frecuencia Moda': series.value_counts().iloc[0] if len(series.value_counts()) > 0 else 0,
            'Nulos': series.isnull().sum()
        }


def print_section_title(title, emoji=""):
    """
    Imprime un título de sección formateado con Streamlit.
    
    Args:
        title (str): Texto del título
        emoji (str): Emoji a mostrar (opcional)
    """
    full_title = f"{emoji} {title}" if emoji else title
    st.markdown(f"## {full_title}")
    st.markdown("---")


def print_subsection_title(title, emoji=""):
    """
    Imprime un subtítulo formateado con Streamlit.
    
    Args:
        title (str): Texto del subtítulo
        emoji (str): Emoji a mostrar (opcional)
    """
    full_title = f"{emoji} {title}" if emoji else title
    st.markdown(f"### {full_title}")


# ============================================================================
# FUNCIONES DE EJEMPLO PARA ENSEÑANZA
# ============================================================================

def ejemplo_fstring():
    """
    Demuestra el uso de f-strings en Python.
    Los f-strings permiten insertar variables directamente en strings.
    """
    nombre = "Juan"
    edad = 25
    promedio = 3.87
    
    # Forma antigua (no recomendada)
    # mensaje = "Hola, mi nombre es " + nombre + " y tengo " + str(edad) + " años"
    
    # Forma moderna con f-strings (RECOMENDADO)
    mensaje = f"Hola, mi nombre es {nombre} y tengo {edad} años"
    
    # F-strings con formato
    mensaje_formateado = f"Promedio: {promedio:.2f}"
    
    return mensaje, mensaje_formateado


def ejemplo_diccionario():
    """
    Demuestra el uso de diccionarios para agrupar información relacionada.
    """
    # Crear diccionario
    persona = {
        'nombre': 'María',
        'edad': 28,
        'ciudad': 'Lima',
        'profesion': 'Ingeniera'
    }
    
    # Acceder a valores
    mensaje = f"{persona['nombre']} es una {persona['profesion']} de {persona['edad']} años"
    
    return persona, mensaje


if __name__ == "__main__":
    # Ejemplos de uso
    print("✅ Módulo utils.py cargado correctamente")
    
    # Probar ejemplo de f-string
    msg1, msg2 = ejemplo_fstring()
    print(msg1)
    print(msg2)
