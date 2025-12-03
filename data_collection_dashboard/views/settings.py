import streamlit as st
import pandas as pd
from datetime import datetime

def show_settings(df, save_callback):
    """Mostrar vista de configuración"""
    st.header("Settings & Configuration")
    
    # Pestañas
    tab1, tab2 = st.tabs(["📁 Data Management", "📤 Import/Export"])
    
    with tab1:
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📚 Load FULL Specification Data", type="primary", use_container_width=True):
                from data_manager import initialize_data
                new_df = initialize_data()
                save_callback(new_df)
                st.success("Full specification data loaded successfully!")
                st.experimental_rerun()
            
            if st.button("➕ Load Sample Data", type="secondary", use_container_width=True):
                from data_manager import initialize_sample_data  # Si tienes esta función
                new_df = initialize_sample_data()
                save_callback(new_df)
                st.success("Sample data loaded!")
                st.experimental_rerun()
        
        with col2:
            if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
                empty_df = pd.DataFrame(columns=df.columns)
                save_callback(empty_df)
                st.success("All data cleared!")
                st.experimental_rerun()
        
    with tab2:
        st.subheader("Import/Export")
        
        # Exportación
        st.write("### Export Data")
        
        export_format = st.selectbox("Export Format:", ["CSV", "Excel"])
        
        if export_format == "CSV":
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"provenance_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                type="primary"
            )
        
        elif export_format == "Excel":
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Data Collection')
            
            st.download_button(
                label="📥 Download Excel",
                data=buffer.getvalue(),
                file_name=f"provenance_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.ms-excel",
                type="primary"
            )