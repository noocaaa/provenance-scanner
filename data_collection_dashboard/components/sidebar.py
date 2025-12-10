import streamlit as st

def show_sidebar(df):
    """Mostrar sidebar con controles y filtros"""
    st.sidebar.header("📊 Dashboard Controls")
    
    # Filtros - manejar DataFrames vacíos
    st.sidebar.subheader("Filters")
    
    # Obtener opciones únicas, manejando DataFrames vacíos
    categories = df["Category"].unique().tolist() if not df.empty else []
    statuses = df["Status"].unique().tolist() if not df.empty else []
    priorities = df["Priority"].unique().tolist() if not df.empty else []
    risks = df["Risk Level"].unique().tolist() if not df.empty else []
    
    # Valores predeterminados seguros
    default_categories = categories[:] if categories else []
    default_statuses = [s for s in ["Pending", "In Progress"] if s in statuses] if statuses else []
    default_priorities = priorities[:] if priorities else []
    default_risks = risks[:] if risks else []
    
    categories_filter = st.sidebar.multiselect(
        "Category",
        options=categories,
        default=default_categories,
        placeholder="Select categories..."
    )
    
    statuses_filter = st.sidebar.multiselect(
        "Status",
        options=statuses,
        default=default_statuses,
        placeholder="Select statuses..."
    )
    
    priorities_filter = st.sidebar.multiselect(
        "Priority",
        options=priorities,
        default=default_priorities,
        placeholder="Select priorities..."
    )
    
    risks_filter = st.sidebar.multiselect(
        "Risk Level",
        options=risks,
        default=default_risks,
        placeholder="Select risk levels..."
    )
    
    # Quick actions
    st.sidebar.subheader("Quick Actions")
    
    if st.sidebar.button("🔄 Refresh All Data", use_container_width=True):
        st.cache_data.clear()
        st.experimental_rerun()
    
    if st.sidebar.button("📊 Generate Summary Report", use_container_width=True):
        st.sidebar.info("Report generation started...")
    
    # Información del sistema
    st.sidebar.divider()
    st.sidebar.subheader("System Info")
    
    if not df.empty:
        total_items = len(df)
        critical_pending = len(df[(df["Priority"] == "Critical") & (df["Status"] == "Pending")])
    else:
        total_items = 0
        critical_pending = 0
    
    st.sidebar.metric("Total Items", total_items)
    st.sidebar.metric("Critical Pending", critical_pending)
    
    return {
        "categories": categories_filter,
        "statuses": statuses_filter,
        "priorities": priorities_filter,
        "risks": risks_filter
    }