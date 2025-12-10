# 🔍 Provenance Scanner - Distributed System Data Collection Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A comprehensive dashboard for mapping, analyzing, and securing distributed systems using structured, automated data collection. Built for security professionals and system administrators to maintain complete visibility over complex IT infrastructures.

## ✨ Features

### 📊 **Comprehensive Data Collection**
- **9 Main Categories** covering all aspects of distributed systems
- **50+ Subcategories** with detailed tracking items
- **Complete specification** based on industry security standards
- **Real-time editing** with validation and risk assessment

### 🎨 **Interactive Dashboard**
- **Multi-tab interface** for different perspectives
- **Advanced filtering** by category, status, priority, and risk level
- **Real-time metrics** and progress tracking
- **Editable data tables** with dynamic row management

### 📈 **Advanced Analytics**
- **Progress visualization** with interactive charts
- **Risk analysis** and priority distribution
- **Timeline views** for due date management
- **Validation status** tracking
- **Custom reports** generation

### ⚙️ **Data Management**
- **Import/Export** capabilities (CSV, Excel, JSON)
- **Sample data** initialization
- **Full specification** data loading
- **Automatic backup** and recovery
- **Data validation** and cleaning

## 🏗️ Project Structure

```
provenance-dashboard/
│
├── app.py # Main Streamlit application
├── data_manager.py # Data loading/saving operations
├── initial_data.py # Complete specification data
├── config.py # Configuration and constants
├── requirements.txt # Python dependencies
├── data_collection_progress.csv # Data storage (auto-generated)
│
├── components/ # Reusable UI components
│ ├── init.py
│ ├── sidebar.py # Sidebar with filters
│ ├── metrics.py # Metric cards
│ └── charts.py # Chart components
│
├── views/ # Application views/pages
│ ├── init.py
│ ├── overview.py # Dashboard overview
│ ├── data_table.py # Editable data table
│ ├── detailed_view.py # Category details
│ ├── analytics.py # Analytics & reports
│ └── settings.py # Settings & configuration
│
└── utils/ # Utility functions
├── init.py
└── helpers.py # Helper functions
└── initial_data.py 

```

## 📋 Data Categories Covered

| Category | Description | Items Count |
|----------|-------------|-------------|
| **1. Asset Inventory** | Hardware, software, and network assets | 18 items |
| **2. System Configuration** | OS settings, users, permissions | 16 items |
| **3. Network Architecture** | Network topology, firewalls, monitoring | 17 items |
| **4. Applications & Services** | Services, APIs, containers, configurations | 17 items |
| **5. Databases** | Database systems and security | 15 items |
| **6. Security & Access** | Authentication, encryption, policies | 18 items |
| **7. Monitoring & Metrics** | System health, alerts, performance | 14 items |
| **8. External Dependencies** | APIs, cloud services, third-party risks | 10 items |
| **9. Special Devices** | Printers, IoT devices, peripherals | 10 items |
| **10. Company Related Data** | Governance, compliance, cloud metadata | 38 items |

**Total: 173+ tracking items**

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/provenance-scanner.git
cd provenance-scanner
```

2. **Create virtual environment** (optional but recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies** 

```bash
pip install -r requirements.txt
```

4. **Run the application** 

```bash
streamlit run app.py
```

5. **Open your browser and navigate to** `http://localhost:8501`

### Dependencies

```bash
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
openpyxl>=3.1.0
```

### Usage Guide

#### Initial Setup

1. Launch the application
2. Go to Settings → Data Management
3. Click "Load FULL Specification Data" to initialize with all categories
4. Start tracking your distributed system components

#### Adding New Items

1. Navigate to Data Collection Table
2. Scroll to the bottom of the table
3. Add new rows directly in the editor
4. Click "Save Changes" to persist

#### Filtering Data

- Use the sidebar filters to focus on specific categories, statuses, or priorities
- Switch between view modes (All Items, By Category, High Priority, Overdue)
- Apply multiple filters simultaneously for precise control

#### Analytics & Reports

- Overview: High-level metrics and progress visualization
- Detailed View: Drill down into specific categories
- Analytics: Generate custom reports and trend analysis
- Export: Download data in CSV, Excel, or JSON format

## Key Features

### Real-time Editing

- Inline editing of all fields
- Dynamic row addition/deletion
- Automatic validation
- Instant save with undo capability

### Risk Assessment

- Automatic risk level assignment based on priority
- Visual risk indicators (color-coded)
- Critical item highlighting
- Risk trend analysis

### Progress Tracking

- Completion percentage by category
- Status distribution visualization
- Due date monitoring
- Validation status tracking

## Dashboard Views 

### 1. Overview Dashboard
- Real-time metrics and KPIs
- Progress charts by category
- Risk distribution visualization
- Timeline view of due dates

### 2. Data Collection Table
- Editable spreadsheet interface
- Bulk operations
- Search and filter capabilities
- Column customization

### 3. Detailed View
- Category-wise breakdown
- Subcategory analysis
- Item-level details
- Custom reports

### 4. Analytics 
- Completion rate analysis
- Risk vs priority matrix
- Timeline analysis

### 5. Settings
- Data management
- Import/export functions
- Dashboard configuration
- System information

## Configuration

### Customizing Categories

Edit `initial_data.py` to:

- Add new categories/subcategories
- Modify priority levels
- Adjust risk assessments
- Customize descriptions

### Dashboard Settings

Access Settings tab to:

- Configure notification preferences
- Set export formats
- Adjust display options
- Manage data retention

## Debug Mode

```bash
streamlit run app.py --logger.level=debug
```