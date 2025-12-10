import streamlit as st
import pandas as pd

def show_detailed_view(df):
    """Mostrar vista detallada"""
    st.header("Detailed View")
    
    if df.empty:
        st.info("No data available for detailed view.")
        return
    
    # Selector de categoría
    categories = df["Category"].unique()
    if len(categories) == 0:
        st.info("No categories available.")
        return
    
    selected_category = st.selectbox(
        "Select Category:",
        categories,
        key="detail_category"
    )
    
    # Filtrar datos
    detail_df = df[df["Category"] == selected_category]
    
    if not detail_df.empty:
        st.subheader(f"Category: {selected_category}")
        
        # Métricas específicas
        cols = st.columns(3)
        
        with cols[0]:
            total = len(detail_df)
            st.metric("Total Items", total)
        
        with cols[1]:
            completed = len(detail_df[detail_df["Status"] == "Completed"])
            st.metric("Completed", completed)
        
        with cols[2]:
            pending = len(detail_df[detail_df["Status"] == "Pending"])
            st.metric("Pending", pending)
        
        # Mostrar subcategorías
        st.subheader("Subcategories")
        
        for subcategory in detail_df["Subcategory"].unique():
            with st.expander(f"📁 {subcategory}"):
                sub_df = detail_df[detail_df["Subcategory"] == subcategory]
                st.dataframe(
                    sub_df[["Item", "Status", "Priority", "Risk Level"]],
                    use_container_width=True
                )
    else:
        st.info(f"No items found for category: {selected_category}")