import pandas as pd
from datetime import datetime, timedelta

def calculate_days_remaining(due_date):
    """Calcular días restantes hasta la fecha de vencimiento"""
    if pd.isna(due_date):
        return None
    return (due_date - pd.Timestamp.now()).days

def format_date(date_value, format_str="%Y-%m-%d"):
    """Formatear fecha para mostrar"""
    if pd.isna(date_value):
        return "Not set"
    return date_value.strftime(format_str)

def get_priority_color(priority):
    """Obtener color basado en prioridad"""
    colors = {
        "Critical": "#FF0000",
        "High": "#FF6B6B",
        "Medium": "#FFD166",
        "Low": "#06D6A0"
    }
    return colors.get(priority, "#CCCCCC")

def get_status_icon(status):
    """Obtener icono basado en estado"""
    icons = {
        "Completed": "✅",
        "In Progress": "🔄",
        "Pending": "⏳",
        "Verified": "☑️",
        "Blocked": "🚫"
    }
    return icons.get(status, "📋")

def validate_item_data(item_data):
    """Validar datos de un item"""
    errors = []
    
    if not item_data.get("Category"):
        errors.append("Category is required")
    if not item_data.get("Item"):
        errors.append("Item name is required")
    if not item_data.get("Priority") in ["Critical", "High", "Medium", "Low"]:
        errors.append("Invalid priority level")
    
    return errors

def generate_summary_stats(df):
    """Generar estadísticas resumidas"""
    stats = {
        "by_status": df["Status"].value_counts().to_dict(),
        "by_priority": df["Priority"].value_counts().to_dict(),
        "by_risk": df["Risk Level"].value_counts().to_dict(),
        "completion_rate": (df["Status"] == "Completed").sum() / len(df) * 100,
        "avg_days_remaining": None
    }
    
    # Calcular días promedio restantes si hay fechas
    if "Due Date" in df.columns:
        days_remaining = df["Due Date"].apply(calculate_days_remaining)
        days_remaining = days_remaining[days_remaining.notna()]
        if not days_remaining.empty:
            stats["avg_days_remaining"] = days_remaining.mean()
    
    return stats