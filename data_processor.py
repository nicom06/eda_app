"""
data_processor.py - Clase principal para procesamiento de datos

Este módulo implementa Programación Orientada a Objetos (POO) con:
- Una clase DataProcessor que encapsula todos los análisis
- Métodos para cada uno de los 10 ítems de análisis
- Uso de NumPy y Pandas para cálculos estadísticos
- F-strings para formateo de mensajes
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Any
from utils import get_column_types, format_number


class DataProcessor:
    """
    Clase para procesar y analizar datasets.
    
    Esta clase encapsula toda la lógica de análisis exploratorio de datos.
    
    Atributos:
        df (pd.DataFrame): El dataframe a analizar
        column_types (dict): Clasificación de columnas por tipo
        
    Ejemplo de uso:
        >>> processor = DataProcessor(mi_dataframe)
        >>> info = processor.get_general_info()
        >>> stats = processor.get_descriptive_statistics()
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Constructor de la clase.
        
        Args:
            dataframe (pd.DataFrame): Dataset a analizar
            
        Raise:
            ValueError: Si el dataframe no es válido
        """
        
        # Validación
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("❌ Se requiere un DataFrame de pandas")
        
        if dataframe.empty:
            raise ValueError("❌ El DataFrame no puede estar vacío")
        
        # Atributos de instancia
        self.df = dataframe
        self.column_types = get_column_types(dataframe)
        
        # Mensaje de confirmación
        print(f"✅ DataProcessor inicializado con {self.df.shape[0]} filas y {self.df.shape[1]} columnas")
    
    # ========================================================================
    # ÍTEM 1: INFORMACIÓN GENERAL DEL DATASET
    # ========================================================================
    
    def get_general_info(self) -> Dict[str, Any]:
        """
        ÍTEM 1: Obtiene información general del dataset.
        
        Incluye:
        - Dimensiones (filas y columnas)
        - Tipos de datos
        - Información de memoria
        - Valores nulos
        
        Returns:
            dict: Información general del dataset
            
        Conceptos aplicados:
        - Métodos de pandas (shape, dtypes, memory_usage)
        - F-strings para formateo
        - Diccionarios para organizar datos
        """
        
        # Usar .info() internamente para obtener detalles
        info_dict = {
            'filas': self.df.shape[0],
            'columnas': self.df.shape[1],
            'memoria_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'columnas_con_nulos': self.df.isnull().sum().sum(),
            'porcentaje_nulos': (self.df.isnull().sum().sum() / 
                                (self.df.shape[0] * self.df.shape[1]) * 100),
            'tipos_datos': self.df.dtypes.value_counts().to_dict()
        }
        
        return info_dict
    
    def get_data_types_summary(self) -> pd.DataFrame:
        """
        Resume los tipos de datos del dataset.
        
        Returns:
            DataFrame con columnas y sus tipos
        """
        
        df_types = pd.DataFrame({
            'Columna': self.df.columns,
            'Tipo': self.df.dtypes.values,
            'No Nulos': self.df.count().values,
            'Nulos': self.df.isnull().sum().values
        })
        
        return df_types
    
    # ========================================================================
    # ÍTEM 2: CLASIFICACIÓN DE VARIABLES
    # ========================================================================
    
    def classify_variables(self) -> Dict[str, List[str]]:
        """
        ÍTEM 2: Clasifica las variables del dataset.
        
        Separa las columnas en:
        - Variables numéricas (int, float)
        - Variables categóricas (object, category)
        - Variables datetime
        - Variables booleanas
        
        Returns:
            dict: Diccionario con listas de variables por tipo
            
        Conceptos aplicados:
        - Lógica de clasificación
        - Diccionarios
        - Métodos de pandas para tipos de datos
        - F-strings para mensajes
        """
        
        # Usar el método ya creado en utils.py
        return self.column_types
    
    def get_variables_summary(self) -> pd.DataFrame:
        """
        Crea un resumen de variables clasificadas.
        
        Returns:
            DataFrame con variable, tipo, conteo único, nulos
        """
        
        summary_data = []
        
        for col in self.df.columns:
            col_type = self.df[col].dtype
            
            # Determinar tipo de variable
            if pd.api.types.is_numeric_dtype(col_type):
                var_type = 'Numérica'
            elif pd.api.types.is_datetime64_any_dtype(col_type):
                var_type = 'Datetime'
            else:
                var_type = 'Categórica'
            
            summary_data.append({
                'Variable': col,
                'Tipo': var_type,
                'Únicos': self.df[col].nunique(),
                'Nulos': self.df[col].isnull().sum(),
                'No Nulos': self.df[col].count()
            })
        
        return pd.DataFrame(summary_data)
    
    # ========================================================================
    # ÍTEM 3: ESTADÍSTICAS DESCRIPTIVAS
    # ========================================================================
    
    def get_descriptive_statistics(self) -> pd.DataFrame:
        """
        ÍTEM 3: Obtiene estadísticas descriptivas del dataset.
        
        Usa .describe() de pandas para:
        - Media (mean)
        - Mediana (50%)
        - Desviación estándar (std)
        - Mínimos y máximos
        - Cuartiles (25%, 50%, 75%)
        
        Returns:
            DataFrame con estadísticas de variables numéricas
            
        Conceptos aplicados:
        - Método .describe() de pandas
        - Estadística descriptiva
        - Interpretación de resultados
        """
        numeric_df = self.df.select_dtypes(include='number')
    
        stats_df = numeric_df.describe().T
        stats_df['Asimetría'] = numeric_df.skew()
        stats_df['Curtosis'] = numeric_df.kurtosis()
        
        return stats_df
        
    def get_numeric_statistics(self) -> pd.DataFrame:
        """
        Obtiene estadísticas detalladas de variables numéricas.
        
        Returns:
            DataFrame con estadísticas completas
        """
        
        numeric_cols = self.df.select_dtypes(include='number').columns.tolist()  # ✅ definir primero
    
        if not numeric_cols:
            return pd.DataFrame()
        
        stats_dict = {}
        
        for col in numeric_cols:
            stats_dict[col] = {
                'Media': self.df[col].mean(),
                'Mediana': self.df[col].median(),
                'Moda': self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else np.nan,
                'Desv. Est.': self.df[col].std(),
                'Varianza': self.df[col].var(),
                'Mínimo': self.df[col].min(),
                'Q1': self.df[col].quantile(0.25),
                'Q3': self.df[col].quantile(0.75),
                'Máximo': self.df[col].max(),
                'Rango': self.df[col].max() - self.df[col].min(),
                'IQR': self.df[col].quantile(0.75) - self.df[col].quantile(0.25)
            }
        
        result_df = pd.DataFrame(stats_dict).T

        #skew y kurtosis solo sobre columnas numéricas
        numeric_df = self.df[numeric_cols]
        result_df['Asimetría'] = numeric_df.skew()
        result_df['Curtosis'] = numeric_df.kurtosis()
        
        return result_df
    
    # ========================================================================
    # ÍTEM 4: ANÁLISIS DE VALORES FALTANTES
    # ========================================================================
    
    def get_missing_values_summary(self) -> pd.DataFrame:
        """
        ÍTEM 4: Analiza valores faltantes en el dataset.
        
        Calcula:
        - Conteo de nulos por columna
        - Porcentaje de nulos
        - Porcentaje de datos válidos
        
        Returns:
            DataFrame con información de valores faltantes
            
        Conceptos aplicados:
        - Método isnull() de pandas
        - Cálculo de porcentajes
        - F-strings para formateo
        """
        
        missing_data = {
            'Columna': self.df.columns,
            'Nulos': self.df.isnull().sum().values,
            'Porcentaje': (self.df.isnull().sum().values / len(self.df) * 100),
            'Válidos': self.df.count().values
        }
        
        missing_df = pd.DataFrame(missing_data)
        
        # Filtrar solo columnas con nulos
        missing_df = missing_df[missing_df['Nulos'] > 0].sort_values('Nulos', ascending=False)
        
        return missing_df
    
    def has_missing_values(self) -> bool:
        """
        Verifica si el dataset tiene valores faltantes.
        
        Returns:
            bool: True si hay nulos, False si no
        """
        
        return self.df.isnull().sum().sum() > 0
    
    def get_missing_percentage(self) -> float:
        """
        Calcula el porcentaje total de valores faltantes.
        
        Returns:
            float: Porcentaje de valores faltantes
        """
        
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing_cells = self.df.isnull().sum().sum()
        
        return (missing_cells / total_cells) * 100
    
    # ========================================================================
    # ÍTEM 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS
    # ========================================================================
    
    def get_numeric_distributions(self) -> Dict[str, Dict[str, float]]:
        """
        ÍTEM 5: Obtiene información de distribuciones numéricas.
        
        Para cada variable numérica calcula:
        - Asimetría (skewness)
        - Curtosis (kurtosis)
        - Rango
        - Coeficiente de variación
        
        Returns:
            dict: Información de distribuciones
            
        Conceptos aplicados:
        - Métodos .skew() y .kurtosis() de pandas
        - NumPy para cálculos estadísticos
        - Diccionarios anidados
        """
        
        distributions = {}
        
        for col in self.column_types['numeric']:
            data = self.df[col].dropna()
            
            distributions[col] = {
                'asimetria': data.skew(),
                'curtosis': data.kurtosis(),
                'rango': data.max() - data.min(),
                'coef_variacion': (data.std() / data.mean()) if data.mean() != 0 else 0
            }
        
        return distributions
    
    # ========================================================================
    # ÍTEM 6: ANÁLISIS DE VARIABLES CATEGÓRICAS
    # ========================================================================
    
    def get_categorical_summary(self, column: str, top_n: int = 10) -> pd.DataFrame:
        """
        ÍTEM 6: Obtiene resumen de variables categóricas.
        
        Calcula:
        - Conteo de frecuencias
        - Porcentajes
        - Proporciones
        
        Args:
            column (str): Nombre de la columna categórica
            top_n (int): Número de categorías principales a mostrar
            
        Returns:
            DataFrame con frecuencias y porcentajes
            
        Conceptos aplicados:
        - Método .value_counts() de pandas
        - Cálculo de proporciones
        """
        
        if column not in self.df.columns:
            raise ValueError(f"❌ Columna '{column}' no existe")
        
        value_counts = self.df[column].value_counts().head(top_n)
        percentages = (value_counts / len(self.df) * 100)
        
        summary_df = pd.DataFrame({
            'Categoría': value_counts.index,
            'Conteo': value_counts.values,
            'Porcentaje': percentages.values,
            'Proporción': (value_counts.values / len(self.df))
        })
        
        return summary_df
    
    def get_all_categorical_summary(self) -> Dict[str, pd.DataFrame]:
        """
        Obtiene resumen de todas las variables categóricas.
        
        Returns:
            dict: Diccionario con resumen de cada variable categórica
        """
        
        categorical_summary = {}
        
        for col in self.column_types['categorical']:
            categorical_summary[col] = self.get_categorical_summary(col)
        
        return categorical_summary
    
    # ========================================================================
    # ÍTEM 7: ANÁLISIS BIVARIADO (NUMÉRICO vs CATEGÓRICO)
    # ========================================================================
    
    def get_numeric_by_category(self, numeric_col: str, categorical_col: str) -> pd.DataFrame:
        """
        ÍTEM 7: Analiza relación entre variable numérica y categórica.
        
        Calcula estadísticas de la variable numérica agrupada por categorías:
        - Media por grupo
        - Mediana por grupo
        - Desviación estándar
        
        Args:
            numeric_col (str): Columna numérica
            categorical_col (str): Columna categórica
            
        Returns:
            DataFrame con estadísticas por grupo
            
        Conceptos aplicados:
        - Método .groupby() de pandas
        - .agg() para agregaciones múltiples
        - Análisis de comparación de grupos
        """
        
        if numeric_col not in self.df.columns or categorical_col not in self.df.columns:
            raise ValueError("❌ Columnas no válidas")
        
        grouped = self.df.groupby(categorical_col)[numeric_col].agg([
            'count',
            'mean',
            'median',
            'std',
            'min',
            'max'
        ]).round(3)
        
        grouped.columns = ['Conteo', 'Media', 'Mediana', 'Desv. Est.', 'Mín', 'Máx']
        
        return grouped
    
    # ========================================================================
    # ÍTEM 8: ANÁLISIS BIVARIADO (CATEGÓRICO vs CATEGÓRICO)
    # ========================================================================
    
    def get_categorical_crosstab(self, col1: str, col2: str) -> pd.DataFrame:
        """
        ÍTEM 8: Crea tabla de contingencia entre dos variables categóricas.
        
        Calcula:
        - Frecuencia conjunta
        - Distribución cruzada
        
        Args:
            col1 (str): Primera columna categórica
            col2 (str): Segunda columna categórica
            
        Returns:
            DataFrame con tabla de contingencia
            
        Conceptos aplicados:
        - Método pd.crosstab()
        - Análisis de asociación categórica
        """
        
        if col1 not in self.df.columns or col2 not in self.df.columns:
            raise ValueError("❌ Columnas no válidas")
        
        crosstab = pd.crosstab(
            self.df[col1],
            self.df[col2],
            margins=True  # Añade márgenes con totales
        )
        
        return crosstab
    
    # ========================================================================
    # ÍTEM 9: ANÁLISIS DINÁMICO (SELECCIÓN DEL USUARIO)
    # ========================================================================
    
    def get_column_statistics(self, column: str) -> Dict[str, Any]:
        """
        ÍTEM 9: Obtiene estadísticas detalladas de una columna específica.
        
        Se adapta al tipo de variable:
        - Numérica: devuelve estadísticas descriptivas
        - Categórica: devuelve distribución de frecuencias
        
        Args:
            column (str): Nombre de la columna
            
        Returns:
            dict: Estadísticas específicas de la columna
            
        Conceptos aplicados:
        - Condicionales basados en tipo de dato
        - Análisis dinámico según entrada del usuario
        - F-strings para mensajes informativos
        """
        
        if column not in self.df.columns:
            raise ValueError(f"❌ Columna '{column}' no existe")
        
        col_data = self.df[column]
        
        # Información común
        stats_dict = {
            'nombre': column,
            'tipo': str(col_data.dtype),
            'conteo': len(col_data),
            'nulos': col_data.isnull().sum(),
            'unicos': col_data.nunique()
        }
        
        # Información específica por tipo
        if pd.api.types.is_numeric_dtype(col_data):
            stats_dict.update({
                'media': col_data.mean(),
                'mediana': col_data.median(),
                'desv_est': col_data.std(),
                'minimo': col_data.min(),
                'maximo': col_data.max(),
                'q1': col_data.quantile(0.25),
                'q3': col_data.quantile(0.75),
                'iqr': col_data.quantile(0.75) - col_data.quantile(0.25)
            })
        else:
            moda = col_data.mode()
            stats_dict.update({
                'moda': moda[0] if len(moda) > 0 else 'N/A',
                'frecuencia_moda': col_data.value_counts().iloc[0] if len(col_data.value_counts()) > 0 else 0
            })
        
        return stats_dict
    
    # ========================================================================
    # ÍTEM 10: HALLAZGOS CLAVE / INSIGHTS
    # ========================================================================
    
    def get_key_findings(self) -> Dict[str, str]:
        """
        ÍTEM 10: Genera hallazgos clave basados en análisis automático.
        
        Identifica:
        - Columnas con muchos nulos
        - Variables con baja variabilidad
        - Columnas con valores atípicos
        - Información de tipos de datos
        
        Returns:
            dict: Diccionario con hallazgos clave
            
        Conceptos aplicados:
        - Lógica de identificación de patrones
        - F-strings para generación de mensajes
        - Análisis automático de características
        """
        
        findings = {}
        
        # Hallazgo 1: Columnas con muchos nulos
        missing_pct = self.get_missing_percentage()
        if missing_pct > 0:
            findings['datos_faltantes'] = (
                f"El dataset contiene {missing_pct:.2f}% de valores faltantes. "
                f"Las columnas más afectadas son: "
                f"{', '.join(self.get_missing_values_summary().head(3)['Columna'].tolist())}"
            )
        else:
            findings['datos_faltantes'] = "No hay valores faltantes en el dataset"
        
        # Hallazgo 2: Distribución de tipos
        findings['tipos_datos'] = (
            f"Dataset con {len(self.column_types['numeric'])} variables numéricas, "
            f"{len(self.column_types['categorical'])} categóricas, "
            f"{len(self.column_types['datetime'])} datetime y "
            f"{len(self.column_types['boolean'])} booleanas."
        )
        
        # Hallazgo 3: Dimensiones
        findings['dimensiones'] = f"Total: {self.df.shape[0]:,} registros × {self.df.shape[1]} variables"
        
        # Hallazgo 4: Variables numéricas
        if self.column_types['numeric']:
            numeric_stats = self.get_numeric_statistics()
            high_var = numeric_stats['Desv. Est.'].idxmax()
            findings['variabilidad'] = (
                f"La variable con mayor variabilidad es '{high_var}' "
                f"(desv. est. = {numeric_stats.loc[high_var, 'Desv. Est.']:.2f})"
            )
        
        # Hallazgo 5: Duplicados
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            findings['duplicados'] = f"Se detectaron {duplicates} filas duplicadas ({duplicates/len(self.df)*100:.2f}%)"
        else:
            findings['duplicados'] = "No se detectaron filas duplicadas"
        
        return findings
    
    # ========================================================================
    # MÉTODOS ADICIONALES ÚTILES
    # ========================================================================
    
    def get_correlation_matrix(self, numeric_only: bool = True) -> pd.DataFrame:
        """
        Calcula la matriz de correlaciones.
        
        Args:
            numeric_only (bool): Si True, solo columnas numéricas
            
        Returns:
            DataFrame: Matriz de correlaciones (Pearson)
        """
        
        if numeric_only:
            return self.df.select_dtypes(include=[np.number]).corr()
        else:
            return self.df.corr(numeric_only=False)
    
    def get_outliers(self, column: str, method: str = 'iqr') -> Dict[str, Any]:
        """
        Detecta valores atípicos en una variable numérica.
        
        Args:
            column (str): Columna numérica
            method (str): 'iqr' o 'zscore'
            
        Returns:
            dict: Información sobre outliers
        """
        
        if column not in self.column_types['numeric']:
            raise ValueError(f"❌ '{column}' no es una variable numérica")
        
        data = self.df[column].dropna()
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(data))
            outliers = data[z_scores > 3]
        
        return {
            'cantidad': len(outliers),
            'porcentaje': len(outliers) / len(data) * 100,
            'valores': outliers.values if len(outliers) > 0 else []
        }


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import pandas as pd
    
    # Crear un dataframe de ejemplo
    np.random.seed(42)
    df_ejemplo = pd.DataFrame({
        'edad': np.random.randint(18, 80, 100),
        'salario': np.random.normal(3000, 1000, 100),
        'ciudad': np.random.choice(['Lima', 'Arequipa', 'Cusco'], 100),
        'educacion': np.random.choice(['Primaria', 'Secundaria', 'Terciaria'], 100)
    })
    
    # Crear instancia de DataProcessor
    processor = DataProcessor(df_ejemplo)
    
    # Usar métodos
    print("\n" + "="*50)
    print("INFORMACIÓN GENERAL")
    print("="*50)
    info = processor.get_general_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*50)
    print("CLASIFICACIÓN DE VARIABLES")
    print("="*50)
    vars_clasificadas = processor.classify_variables()
    for tipo, cols in vars_clasificadas.items():
        print(f"{tipo}: {cols}")
    
    print("\n DataProcessor funcionando correctamente")
