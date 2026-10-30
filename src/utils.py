"""
Módulo de utilidades para el análisis de Vaca Muerta.
Autor: Deysi Carolina Bailon Trujillo
Perfil: Junior Data Analyst | Business AI Builder
"""
import plotly.io as pio
import pandas as pd
import os

def set_global_style():
    """Configura el template visual y la paleta de colores para todo el proyecto."""
    pio.templates.default = "plotly_white"
    pio.templates["plotly_white"].layout.colorway = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#7f7f7f'
    ]
    pio.templates["plotly_white"].layout.font.family = "Arial, sans-serif"

def cargar_datos(nombre_archivo):
    """
    Carga los datos desde la carpeta 'data/'.
    """
    # Al ejecutar desde notebooks/, subimos un nivel (..) y entramos a data/
    ruta = os.path.join("..", "data", nombre_archivo)
    
    if not os.path.exists(ruta):
        print(f"❌ Error: No se encontró el dataset en '{ruta}'.")
        return pd.DataFrame()
        
    print(f"📥 Cargando datos desde '{ruta}'...")
    df = pd.read_csv(ruta)
    
    # Estandarización de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Optimización de memoria
    mem_antes = df.memory_usage(deep=True).sum() / 1024**2
    
    cols_int = df.select_dtypes(include=['int64']).columns
    df[cols_int] = df[cols_int].apply(pd.to_numeric, downcast='integer')
    
    cols_float = df.select_dtypes(include=['float64']).columns
    df[cols_float] = df[cols_float].apply(pd.to_numeric, downcast='float')
    
    mem_despues = df.memory_usage(deep=True).sum() / 1024**2
    
    print(f"✅ Dataset cargado. Dimensiones: {df.shape}")
    print(f"💾 Memoria optimizada: de {mem_antes:.2f} MB a {mem_despues:.2f} MB")
    
    return df