import streamlit as st
import pandas as pd
from components.metrics import show_metrics
from components.charts import create_pie_chart, create_bar_chart

def show_overview(filtered_df, full_df):
    """Mostrar vista Overview"""
    st.header("Overview Dashboard")
    
    if filtered_df.empty:
        st.info("No data available with current filters. Try adjusting your filters or add new data.")
        return
    
    # Métricas principales
    metrics = show_metrics(filtered_df)
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Progress by Category")
        if not filtered_df.empty:
            category_progress = filtered_df.groupby("Category")["Status"].apply(
                lambda x: (x == "Completed").sum() / len(x) * 100 if len(x) > 0 else 0
            ).reset_index()
            category_progress.columns = ["Category", "Completion %"]
            
            if not category_progress.empty:
                fig1 = create_bar_chart(category_progress, "Category", "Completion %", "Completion % by Category")
                if fig1:
                    st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Risk Distribution")
        fig2 = create_pie_chart(filtered_df, "Risk Level", "Risk Level Distribution")
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
    
    # Gráficos adicionales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Status Distribution")
        fig_status = create_pie_chart(filtered_df, "Status", "Status Distribution")
        if fig_status:
            st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        st.subheader("Priority Distribution")
        fig_priority = create_pie_chart(filtered_df, "Priority", "Priority Distribution")
        if fig_priority:
            st.plotly_chart(fig_priority, use_container_width=True)