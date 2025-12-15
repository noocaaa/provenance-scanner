import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utils.initial_data import get_full_initial_data

@st.cache_data
def load_data():
    """Cargar datos desde CSV o inicializar si no existe"""
    try:
        df = pd.read_csv("data/data_collection_progress.csv")
        
        # Asegurar tipos de datos correctos
        if "Due Date" in df.columns:
            df["Due Date"] = pd.to_datetime(df["Due Date"], errors='coerce')
        
        # Asegurar que Notes sea string, no float
        if "Notes" in df.columns:
            df["Notes"] = df["Notes"].astype(str).replace('nan', '').replace('None', '')
        
        return df
    except FileNotFoundError:
        return pd.DataFrame()  # Devolver DataFrame vacío

def save_data(df):
    """Guardar datos en CSV"""
    # Asegurar tipos antes de guardar
    if "Notes" in df.columns:
        df["Notes"] = df["Notes"].astype(str).fillna('')
    
    df.to_csv("data/data_collection_progress.csv", index=False)
    st.session_state['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def initialize_data():
    """Inicializar datos con TODA la especificación"""
    from datetime import datetime
    
    # Obtener todos los datos de la especificación
    initial_items = get_full_initial_data()
    
    # Crear DataFrame con valores predeterminados
    data = []
    
    for item in initial_items:
        data.append({
            "Category": item["Category"],
            "Subcategory": item["Subcategory"],
            "Item": item["Item"],
            "Description": item["Description"],
            "Type": item["Type"],
            "Priority": item["Priority"],
            "Status": "Pending",  # Por defecto
            "Due Date": datetime.now() + timedelta(days=30),
            "Notes": "",
            "Risk Level": item["Risk Level"],
            "Validation Status": "Not Validated"
        })
    
    df = pd.DataFrame(data)
    save_data(df)
    return df