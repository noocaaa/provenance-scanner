import streamlit as st
import pandas as pd
from datetime import datetime

def show_data_table(filtered_df, full_df, save_callback):
    """Mostrar vista de tabla de datos"""
    st.header("Data Collection Table")
    
    if filtered_df.empty:
        st.info("No data available with current filters.")
        
        if st.button("➕ Add Sample Data", type="primary"):
            from data_manager import initialize_data
            new_df = initialize_data()
            save_callback(new_df)
            st.experimental_rerun()
        return
    
    # Opciones de visualización
    view_mode = st.radio(
        "View Mode:",
        ["All Items", "By Category", "High Priority", "Overdue"],
        horizontal=True
    )
    
    # Filtrar según modo de vista
    display_df = filtered_df.copy()
    
    if view_mode == "By Category":
        categories = filtered_df["Category"].unique()
        if len(categories) > 0:
            selected_category = st.selectbox("Select Category:", categories)
            display_df = display_df[display_df["Category"] == selected_category]
    
    elif view_mode == "High Priority":
        display_df = display_df[display_df["Priority"].isin(["Critical", "High"])]
    
    elif view_mode == "Overdue":
        if "Due Date" in display_df.columns:
            display_df = display_df[(display_df["Due Date"] < pd.Timestamp.now()) & 
                                   (display_df["Status"] != "Completed")]
    
    # Editor de datos
    st.subheader("Edit Collection Items")
    
    # Configurar columnas editables
    # Busca esta sección y cambia la configuración de "Notes":
    column_config = {
        "Item": st.column_config.TextColumn("Item"),
        "Description": st.column_config.TextColumn("Description"),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Pending", "In Progress", "Completed", "Verified", "Blocked"]
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            options=["Critical", "High", "Medium", "Low"]
        ),
        "Due Date": st.column_config.DateColumn("Due Date"),
        "Risk Level": st.column_config.SelectboxColumn(
            "Risk Level",
            options=["Critical", "High", "Medium", "Low"]
        ),
        "Validation Status": st.column_config.SelectboxColumn(
            "Validation Status",
            options=["Not Validated", "Validated", "Failed", "In Review"]
        ),
        # CORREGIR ESTO: Asegurar que Notes maneje cualquier tipo de dato
        "Notes": st.column_config.TextColumn("Notes"),
    }
        
    edited_df = st.data_editor(
        display_df,
        column_config=column_config,
        use_container_width=True,
        height=400,
        num_rows="dynamic",
        key="data_editor"
    )
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            # Encontrar índices de las filas editadas y actualizar el DataFrame original
            for idx in edited_df.index:
                if idx in full_df.index:
                    for col in edited_df.columns:
                        full_df.at[idx, col] = edited_df.at[idx, col]
            
            save_callback(full_df)
            st.success("Changes saved successfully!")
            st.experimental_rerun()
    
    with col2:
        if st.button("🔄 Discard Changes", use_container_width=True):
            st.experimental_rerun()
    
    with col3:
        csv = full_df.to_csv(index=False)
        st.download_button(
            label="📥 Export CSV",
            data=csv,
            file_name="data_collection_export.csv",
            mime="text/csv",
            use_container_width=True
        )