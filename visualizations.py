"""
visualizations.py - Funciones de visualización

Este módulo contiene funciones para crear gráficos interactivos y estáticos usando:
- Matplotlib y Seaborn: gráficos estáticos de alta calidad
- Plotly: gráficos interactivos que funcionan en Streamlit
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Tuple


# Configurar estilo por defecto
sns.set_style("whitegrid")
sns.set_palette("husl")


class DataVisualizations:
    """
    Clase para crear visualizaciones de datos.
    
    Contiene métodos para generar gráficos interactivos con Plotly
    que se integran perfectamente con Streamlit.
    
    Atributos:
        df (pd.DataFrame): El dataframe a visualizar
        
    Ejemplo:
        >>> viz = DataVisualizations(mi_dataframe)
        >>> fig = viz.create_histogram('edad')
        >>> st.plotly_chart(fig)
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Constructor.
        
        Args:
            dataframe (pd.DataFrame): Dataframe a visualizar
        """
        self.df = dataframe
    
    # ========================================================================
    # DISTRIBUCIONES DE VARIABLES NUMÉRICAS (ÍTEM 5)
    # ========================================================================
    
    def create_histogram(self, column: str, nbins: int = 30) -> go.Figure:
        """
        Crea un histograma interactivo para variable numérica.
        
        Args:
            column (str): Nombre de la columna
            nbins (int): Número de bins (default: 30)
            
        Returns:
            plotly.graph_objects.Figure: Gráfico interactivo
            
        Conceptos:
        - Distribución de frecuencias
        - Histogramas con Plotly
        """
        
        data = self.df[column].dropna()
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=nbins,
            name=column,
            marker=dict(
                color='rgba(55, 128, 191, 0.7)',
                line=dict(color='rgba(55, 128, 191, 1)', width=1.5)
            )
        ))
        
        fig.update_layout(
            title=f"<b>Distribución de {column}</b>",
            xaxis_title=column,
            yaxis_title="Frecuencia",
            hovermode='x unified',
            template="plotly_white",
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_boxplot(self, column: str, group_by: Optional[str] = None) -> go.Figure:
        """
        Crea un boxplot para analizar la distribución y outliers.
        
        Args:
            column (str): Columna numérica a analizar
            group_by (str): Columna para agrupar (opcional)
            
        Returns:
            plotly.graph_objects.Figure: Boxplot interactivo
            
        Conceptos:
        - Visualización de cuartiles
        - Detección de outliers
        - Comparación por grupos
        """
        
        fig = go.Figure()
        
        if group_by is None:
            # Boxplot simple
            fig.add_trace(go.Box(
                y=self.df[column].dropna(),
                name=column,
                boxmean='sd'
            ))
        else:
            # Boxplot por grupos
            for group in sorted(self.df[group_by].unique()):
                data = self.df[self.df[group_by] == group][column]
                fig.add_trace(go.Box(
                    y=data,
                    name=str(group),
                    boxmean='sd'
                ))
        
        fig.update_layout(
            title=f"<b>Boxplot de {column}</b>",
            yaxis_title=column,
            template="plotly_white",
            height=500,
            hovermode='y unified'
        )
        
        return fig
    
    def create_violin_plot(self, column: str, group_by: Optional[str] = None) -> go.Figure:
        """
        Crea un violin plot para mostrar distribuciones.
        
        Args:
            column (str): Columna numérica
            group_by (str): Columna para agrupar
            
        Returns:
            plotly.graph_objects.Figure: Violin plot
        """
        
        if group_by is None:
            fig = px.violin(self.df, y=column, box=True, points="outliers")
        else:
            fig = px.violin(
                self.df,
                x=group_by,
                y=column,
                box=True,
                points="outliers"
            )
        
        fig.update_layout(
            title=f"<b>Distribución de {column}</b>",
            template="plotly_white",
            height=500
        )
        
        return fig
    
    # ========================================================================
    # VARIABLES CATEGÓRICAS (ÍTEM 6)
    # ========================================================================
    
    def create_bar_chart(self, column: str, top_n: int = 10, 
                        horizontal: bool = False) -> go.Figure:
        """
        Crea un gráfico de barras para variable categórica.
        
        Args:
            column (str): Columna categórica
            top_n (int): Top N categorías a mostrar
            horizontal (bool): Si True, barras horizontales
            
        Returns:
            plotly.graph_objects.Figure: Gráfico de barras
            
        Conceptos:
        - Conteo de frecuencias con .value_counts()
        - Visualización de proporciones
        """
        
        value_counts = self.df[column].value_counts().head(top_n)
        percentages = (value_counts / len(self.df) * 100)
        
        fig = go.Figure()
        
        if horizontal:
            fig.add_trace(go.Bar(
                y=value_counts.index,
                x=value_counts.values,
                orientation='h',
                text=value_counts.values,
                textposition='auto',
                marker=dict(color='lightblue'),
                hovertemplate='<b>%{y}</b><br>Conteo: %{x}<extra></extra>'
            ))
        else:
            fig.add_trace(go.Bar(
                x=value_counts.index,
                y=value_counts.values,
                text=value_counts.values,
                textposition='outside',
                marker=dict(color='lightblue'),
                hovertemplate='<b>%{x}</b><br>Conteo: %{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title=f"<b>Distribución de {column}</b>",
            xaxis_title=column if not horizontal else "Conteo",
            yaxis_title="Conteo" if not horizontal else column,
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_pie_chart(self, column: str, top_n: int = 10) -> go.Figure:
        """
        Crea un gráfico de pastel.
        
        Args:
            column (str): Columna categórica
            top_n (int): Top N categorías
            
        Returns:
            plotly.graph_objects.Figure: Pie chart
        """
        
        value_counts = self.df[column].value_counts().head(top_n)
        
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hovertemplate='<b>%{label}</b><br>Conteo: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f"<b>Proporción de {column}</b>",
            height=500
        )
        
        return fig
    
    # ========================================================================
    # ANÁLISIS BIVARIADO (ÍTEMS 7-8)
    # ========================================================================
    
    def create_scatter_plot(self, x_col: str, y_col: str, 
                           color_col: Optional[str] = None,
                           size_col: Optional[str] = None) -> go.Figure:
        """
        Crea un scatter plot para relación entre dos variables numéricas.
        
        Args:
            x_col (str): Columna para eje X
            y_col (str): Columna para eje Y
            color_col (str): Columna para colorear puntos (opcional)
            size_col (str): Columna para tamaño de puntos (opcional)
            
        Returns:
            plotly.graph_objects.Figure: Scatter plot
            
        Conceptos:
        - Relación entre variables
        - Correlación visual
        """
        
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col,
            hover_data=[x_col, y_col],
            trendline="ols",  # Añade línea de tendencia
            template="plotly_white"
        )
        
        fig.update_layout(
            title=f"<b>Relación: {x_col} vs {y_col}</b>",
            height=500,
            hovermode='closest'
        )
        
        return fig
    
    def create_categorical_boxplot(self, x_col: str, y_col: str) -> go.Figure:
        """
        Crea boxplot para variable numérica por categoría.
        
        Usado en ÍTEM 7 (numérico vs categórico)
        
        Args:
            x_col (str): Columna categórica
            y_col (str): Columna numérica
            
        Returns:
            plotly.graph_objects.Figure: Boxplot por grupo
        """
        
        fig = px.box(
            self.df,
            x=x_col,
            y=y_col,
            points="outliers"
        )
        
        fig.update_layout(
            title=f"<b>{y_col} por {x_col}</b>",
            template="plotly_white",
            height=500
        )
        
        return fig
    
    def create_heatmap_crosstab(self, x_col: str, y_col: str) -> go.Figure:
        """
        Crea heatmap de tabla de contingencia (ÍTEM 8).
        
        Usado para variables categóricas
        
        Args:
            x_col (str): Primera columna categórica
            y_col (str): Segunda columna categórica
            
        Returns:
            plotly.graph_objects.Figure: Heatmap
        """
        
        crosstab = pd.crosstab(self.df[x_col], self.df[y_col])
        
        fig = go.Figure(data=go.Heatmap(
            z=crosstab.values,
            x=crosstab.columns,
            y=crosstab.index,
            colorscale='Blues',
            text=crosstab.values,
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='%{y} - %{x}: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"<b>Tabla de Contingencia: {x_col} vs {y_col}</b>",
            xaxis_title=y_col,
            yaxis_title=x_col,
            height=500
        )
        
        return fig
    
    # ========================================================================
    # MATRIZ DE CORRELACIONES
    # ========================================================================
    
    def create_correlation_heatmap(self, corr_matrix: pd.DataFrame) -> go.Figure:
        """
        Crea heatmap de matriz de correlaciones.
        
        Args:
            corr_matrix (pd.DataFrame): Matriz de correlación
            
        Returns:
            plotly.graph_objects.Figure: Heatmap de correlaciones
        """
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            zmin=-1,
            zmax=1,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 9},
            hovertemplate='%{y} - %{x}: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Matriz de Correlaciones de Pearson</b>",
            width=700,
            height=600
        )
        
        return fig
    
    # ========================================================================
    # VALORES FALTANTES (ÍTEM 4)
    # ========================================================================
    
    def create_missing_values_bar(self) -> go.Figure:
        """
        Crea gráfico de valores faltantes.
        
        Args:
            
        Returns:
            plotly.graph_objects.Figure: Gráfico de barras
        """
        
        missing_data = self.df.isnull().sum()
        missing_pct = (missing_data / len(self.df) * 100)
        
        # Filtrar solo columnas con nulos
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        missing_pct = missing_pct[missing_data.index]
        
        if len(missing_data) == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="✅ No hay valores faltantes",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20)
            )
            return fig
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=missing_data.index,
            y=missing_pct.values,
            text=missing_pct.round(2),
            textposition='outside',
            marker=dict(color='#FF6B6B'),
            hovertemplate='<b>%{x}</b><br>Faltantes: %{y:.2f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Porcentaje de Valores Faltantes por Columna</b>",
            xaxis_title="Columna",
            yaxis_title="Porcentaje (%)",
            template="plotly_white",
            height=500
        )
        
        return fig
    
    # ========================================================================
    # GRÁFICOS COMPARATIVOS
    # ========================================================================
    
    def create_comparison_histogram(self, column: str, group_by: str) -> go.Figure:
        """
        Crea histograma superpuesto por grupo.
        
        Args:
            column (str): Columna numérica a visualizar
            group_by (str): Columna para agrupar
            
        Returns:
            plotly.graph_objects.Figure: Histogramas comparativos
        """
        
        fig = px.histogram(
            self.df,
            x=column,
            color=group_by,
            nbins=30,
            barmode='overlay'
        )
        
        fig.update_layout(
            title=f"<b>Distribución de {column} por {group_by}</b>",
            xaxis_title=column,
            yaxis_title="Frecuencia",
            template="plotly_white",
            height=500,
            barmode='overlay'
        )
        
        return fig
    
    def create_count_plot(self, column: str) -> go.Figure:
        """
        Crea gráfico de conteos (similar a countplot de seaborn).
        
        Args:
            column (str): Columna categórica
            
        Returns:
            plotly.graph_objects.Figure: Gráfico de conteos
        """
        
        counts = self.df[column].value_counts().reset_index()
        counts.columns = ['categoria', 'conteo']
        
        fig = px.bar(
            counts,
            x='categoria',
            y='conteo',
            text='conteo'
        )
        
        fig.update_traces(textposition='outside')
        
        fig.update_layout(
            title=f"<b>Conteo de {column}</b>",
            xaxis_title=column,
            yaxis_title="Conteo",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        return fig
    
    # ========================================================================
    # GRÁFICOS CON MATPLOTLIB Y SEABORN (Estáticos)
    # ========================================================================
    
    @staticmethod
    def create_matplotlib_distribution(data, title: str = "Distribución", 
                                      figsize: Tuple[int, int] = (10, 6)):
        """
        Crea histograma con matplotlib y seaborn.
        
        Args:
            data: Series de pandas
            title (str): Título del gráfico
            figsize (tuple): Tamaño de la figura
            
        Returns:
            matplotlib.figure.Figure: Figura
            
        Nota: Usar con st.pyplot() en Streamlit
        """
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.histplot(data, kde=True, ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_matplotlib_boxplot(data, labels: list, title: str = "Boxplot",
                                 figsize: Tuple[int, int] = (10, 6)):
        """
        Crea boxplot con matplotlib.
        
        Args:
            data: Lista de series o arrays
            labels (list): Etiquetas para cada box
            title (str): Título
            figsize (tuple): Tamaño
            
        Returns:
            matplotlib.figure.Figure: Figura
        """
        
        fig, ax = plt.subplots(figsize=figsize)
        
        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        
        # Colorear
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel("Valor")
        
        plt.tight_layout()
        return fig


# ============================================================================
# FUNCIONES AUXILIARES PARA GRÁFICOS
# ============================================================================

def set_plot_style(style: str = "whitegrid", palette: str = "husl"):
    """
    Configura el estilo global de Seaborn.
    
    Args:
        style (str): Estilo a usar ('whitegrid', 'darkgrid', 'dark', 'white')
        palette (str): Paleta de colores
    """
    sns.set_style(style)
    sns.set_palette(palette)


def configure_plotly_theme(template: str = "plotly_white"):
    """
    Configura tema por defecto para Plotly.
    
    Args:
        template (str): Tema a usar
    """
    # Puede usarse en cada figura si se requiere
    pass


if __name__ == "__main__":
    # Ejemplo de uso
    np.random.seed(42)
    df_test = pd.DataFrame({
        'edad': np.random.normal(35, 15, 200),
        'salario': np.random.normal(50000, 20000, 200),
        'ciudad': np.random.choice(['Lima', 'Arequipa', 'Cusco'], 200),
        'educacion': np.random.choice(['Primaria', 'Secundaria', 'Terciaria'], 200)
    })
    
    viz = DataVisualizations(df_test)
    
    print("✅ Módulo visualizations.py cargado correctamente")
    print(f"Disponibles: histograma, boxplot, scatter, heatmap, etc.")
