# SalesInsight – Automated Sales Reporting Tool

**SalesInsight** is a python-based project with the ability to automate the process of analyzing sales data and generating visual reports. It loads CSV or Excel data, processes it using popular data science libraries, and outputs clean, interpretable charts and summaries for business use.

---------

# Features

- Import sales data from `.xlsx` or `.csv` files  
- Clean and preprocess raw sales records  
- Generate KPIs such as revenue trends, top products, and regional performance  
- Create visual charts (bar plots, pie charts, line graphs)  
- Export reports as PNG or PDF (optional)  
- Optional: Streamlit interface for non-technical users

---

# Project Structure

Sales-insight-report/

├── data/      # Sample or uploaded sales data

├── src/       # Source code (data loading, analysis, visualization)

├── reports/   # Generated reports or exported charts

├── LICENSE

├── README.md

├── requirements.txt

└── .gitignore

---

# Example KPIs

- Monthly revenue trends
- Top 5 selling products
- Revenue by region or product category
- Performance of individual sales representatives

---

# Tech Stack

- Language:      Python 3.10+
- Data Library:  pandas
- File Handling: pathlib, os
- Visualization: matplotlib
- UI:            Streamlit

---

# How to Run

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
# On Windows run:
venv\Scripts\activate
# On Unix (macOS, linux, WSL) run:
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
