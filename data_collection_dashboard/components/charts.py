import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_pie_chart(df, column, title):
    """Crear gráfico de pastel"""
    if df.empty or column not in df.columns:
        return None
    
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, "Count"]
    
    fig = px.pie(
        value_counts, 
        values="Count", 
        names=column,
        title=title
    )
    return fig

def create_bar_chart(df, x_column, y_column, title, color_column=None):
    """Crear gráfico de barras"""
    if df.empty or x_column not in df.columns or y_column not in df.columns:
        return None
    
    if color_column and color_column in df.columns:
        fig = px.bar(
            df, 
            x=x_column, 
            y=y_column,
            color=color_column,
            title=title,
            barmode="group"
        )
    else:
        fig = px.bar(df, x=x_column, y=y_column, title=title)
    
    return fig