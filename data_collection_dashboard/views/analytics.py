import streamlit as st
import pandas as pd

def show_analytics(df):
    """Mostrar vista de analytics"""
    st.header("Analytics & Reports")
    
    if df.empty:
        st.info("No data available for analytics.")
        return
    
    # Reporte simple
    st.subheader("Basic Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Status Distribution:**")
        status_counts = df["Status"].value_counts()
        st.dataframe(status_counts)
    
    with col2:
        st.write("**Priority Distribution:**")
        priority_counts = df["Priority"].value_counts()
        st.dataframe(priority_counts)
    
    # Por categoría
    st.subheader("By Category")
    
    for category in df["Category"].unique():
        with st.expander(f"📊 {category}"):
            cat_df = df[df["Category"] == category]
            
            cols = st.columns(3)
            with cols[0]:
                st.metric("Total", len(cat_df))
            with cols[1]:
                completed = len(cat_df[cat_df["Status"] == "Completed"])
                st.metric("Completed", completed)
            with cols[2]:
                pending = len(cat_df[cat_df["Status"] == "Pending"])
                st.metric("Pending", pending)