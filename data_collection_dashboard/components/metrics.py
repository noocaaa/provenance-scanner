import streamlit as st
import pandas as pd

def show_metrics(df):
    """Mostrar métricas principales"""
    if df.empty:
        st.warning("No data available")
        return {"total": 0, "completed": 0, "critical": 0, "overdue": 0}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = len(df)
        st.metric("Total Items", total_items)
    
    with col2:
        completed = len(df[df["Status"] == "Completed"])
        completion_rate = (completed/total_items*100) if total_items > 0 else 0
        st.metric("Completed", f"{completed} ({completion_rate:.1f}%)")
    
    with col3:
        critical_items = len(df[df["Priority"] == "Critical"])
        st.metric("Critical Items", critical_items)
    
    with col4:
        overdue = len(df[(df["Due Date"] < pd.Timestamp.now()) & (df["Status"] != "Completed")])
        st.metric("Overdue", overdue, delta_color="inverse")
    
    return {
        "total": total_items,
        "completed": completed,
        "critical": critical_items,
        "overdue": overdue
    }