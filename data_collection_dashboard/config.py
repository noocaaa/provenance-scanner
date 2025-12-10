# Opciones para dropdowns
STATUS_OPTIONS = ["Pending", "In Progress", "Completed", "Verified", "Blocked"]
PRIORITY_OPTIONS = ["Critical", "High", "Medium", "Low"]
RISK_LEVEL_OPTIONS = ["Critical", "High", "Medium", "Low"]
VALIDATION_OPTIONS = ["Not Validated", "Validated", "Failed", "In Review"]
TYPE_OPTIONS = ["Static", "Dynamic", "Static+Dynamic"]

# Configuración de columnas para data_editor
COLUMN_CONFIG = {
    "Status": {"options": STATUS_OPTIONS},
    "Priority": {"options": PRIORITY_OPTIONS},
    "Risk Level": {"options": RISK_LEVEL_OPTIONS},
    "Validation Status": {"options": VALIDATION_OPTIONS},
}

# Mapeo de colores para gráficos
COLOR_SCALES = {
    "status": {"Completed": "#00C851", "In Progress": "#FFBB33", "Pending": "#FF4444", "Verified": "#33b5e5", "Blocked": "#ff4444"},
    "priority": {"Critical": "#CC0000", "High": "#FF4444", "Medium": "#FFBB33", "Low": "#00C851"},
    "risk": {"Critical": "#CC0000", "High": "#FF4444", "Medium": "#FFBB33", "Low": "#00C851"}
}

# Categorías base (simplificadas para empezar)
BASE_CATEGORIES = [
    "Asset Inventory",
    "System Configuration", 
    "Network Architecture",
    "Applications and Services",
    "Databases",
    "Security and Access",
    "Monitoring and Metrics",
    "External Dependencies",
    "Special Devices",
    "Company Related Data"
]