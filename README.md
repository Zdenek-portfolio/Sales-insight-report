# Sales Insight – Data Analysis Tool

**SalesInsight** is a Python-based tool designed to automate sales data analysis and create visual reports. The program processes Excel and CSV files and generates insightful charts, enabling businesses to make informed decisions based on their sales performance.

---

## Features

- Import sales data from `.xlsx` or `.csv` files  
- Generate KPIs (e.g. *pie, line,* and *bar charts*)
- Display analysis in Streamlit with download option  
- Optionally export charts via terminal (both options save charts as `.png` files)  

---

## Tech Stack

- **Language**: Python 3.10+
- **Data Handling**: pandas, openpyxl
- **File Handling**: pathlib, os
- **Visualization**: Plotly
- **Exporting**: Kaleido
- **UI**: Streamlit

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

## How to Run

1. Download and extract the `.zip` file.
2. Locate the folder directory in your terminal
3. Create a virtual environment:
```bash
python -m venv venv
```
   
4. Activate the virtual environment:

  - On Windows:
    ```bash
    venv\Scripts\activate
    ```

  - On macOS/Linux/WSL:
    ```bash
    source venv/bin/activate
    ```
   
5. Install dependencies:
```bash
pip install -r requirements.txt
```
   
6. Run the app:
```bash
streamlit run src/display.py
```

##

To download the charts via terminal (*steps 1–5 remain the same*):

6. Run the script
```bash
python src/download.py
```
