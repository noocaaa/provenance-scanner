import streamlit as st
import pandas as pd
from views.overview import show_overview
from views.data_table import show_data_table
from views.detailed_view import show_detailed_view
from views.analytics import show_analytics
from views.settings import show_settings
from components.sidebar import show_sidebar
from data_manager import load_data, save_data, initialize_data

# Configuración de página
st.set_page_config(
    page_title="Provenance Scanner - Distributed System Data Collection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título y descripción
st.title("🔍 Provenance Scanner - Distributed System Data Collection")
st.markdown("""
*Project*: Provenance Scanner  
*Purpose*: Map, analyze, and secure distributed systems using structured, automated data collection.
*Version*: 1.0
""")

# Cargar datos
df = load_data()

# Verificar si el DataFrame está vacío
if df.empty:
    st.warning("⚠️ No data found. Initializing with default data...")
    df = initialize_data()
    save_data(df)
    st.experimental_rerun()

# Mostrar sidebar y obtener filtros
filters = show_sidebar(df)

# Aplicar filtros (manejar casos donde no hay valores)
filtered_df = df.copy()

if not df.empty:
    if filters["categories"]:
        filtered_df = filtered_df[filtered_df["Category"].isin(filters["categories"])]
    
    if filters["statuses"]:
        filtered_df = filtered_df[filtered_df["Status"].isin(filters["statuses"])]
    
    if filters["priorities"]:
        filtered_df = filtered_df[filtered_df["Priority"].isin(filters["priorities"])]
    
    if filters["risks"]:
        filtered_df = filtered_df[filtered_df["Risk Level"].isin(filters["risks"])]

# Pestañas principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview Dashboard",
    "📋 Data Collection Table",
    "🔍 Detailed View",
    "📊 Analytics",
    "⚙️ Settings"
])

# Mostrar cada vista
with tab1:
    show_overview(filtered_df, df)

with tab2:
    show_data_table(filtered_df, df, save_data)

with tab3:
    show_detailed_view(filtered_df)

with tab4:
    show_analytics(filtered_df)

with tab5:
    show_settings(df, save_data)

# Footer
st.divider()
from datetime import datetime
st.caption(f"""
**Provenance Scanner Dashboard** | *Distributed System Data Collection*  
*Last Updated:* {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | *Total Items Tracked:* {len(df)}
""")