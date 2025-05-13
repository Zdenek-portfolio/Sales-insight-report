# *SalesInsight* – Automated Sales Reporting Tool

**SalesInsight** is a python-based project with the ability to automate the process of analyzing sales data and generating visual reports. It loads Excel or CSV data, processes it using popular data science libraries, and outputs clean, interpretable charts and summaries for business use.

---

## Features

- Import sales data from `.xlsx` or `.csv` files  
- Generate KPIs if required columns are present  
- Create line, pie, and bar charts  
- Display analysis in Streamlit with download option  
- Optionally export charts via terminal (both options save charts as `.png` files)  

---

## Data Requirements for KPI Charts

*Each chart requires the listed columns to be present in the dataset.*

- **Total Revenue Overview**: `Revenue`, `Date`  
- **Monthly Revenue Trends**: `Revenue`, `Date`  
- **Regional Revenue Breakdown**: `Revenue`, `Region`  
- **Revenue by Product Category**: `Revenue`, `Category`  
- **Top 5 Revenue-Generating Products**: `Revenue`, `Product`  
- **Top 5 Best-Selling Products (by Units Sold)**: `Quantity`, `Product`  
- **Units Sold per Product Category**: `Quantity`, `Category`

---

## Tech Stack

- Language:      Python 3.10+
- Data Library:  pandas
- File Handling: pathlib, os
- Visualization: matplotlib
- UI:            Streamlit

---

## How to Run

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
# Activate the VE on Windows:
venv\Scripts\activate
# Activate the VE on Unix (macOS, linux, WSL):
source venv/bin/activate   

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the main script
python src/main.py
```

Or run the Streamlit UI

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

---

# Environment Variables
Create a .env file if you use API keys or credentials (e.g. for emailing reports or accessing cloud storage).

EMAIL_USER="your@email.com"
EMAIL_PASS="yourpassword"
