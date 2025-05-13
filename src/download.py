import pandas as pd
import plotly.express as px
import os
import time
import sys

print()

COLOR_PALETTE = px.colors.qualitative.Set2
REPORTS_DIR = "reports"
DATA_DIR = "data"
PLACEHOLDER_FILE = os.path.join(REPORTS_DIR, "placeholder.txt")

os.makedirs(REPORTS_DIR, exist_ok=True)

# Check if placeholder file exists
placeholder_exists = os.path.isfile(PLACEHOLDER_FILE)

# Find a file to use
available_files = [f for f in os.listdir(DATA_DIR) if f.endswith((".csv", ".xlsx"))]
if not available_files:
    print("No data files found in the 'data/' folder.")
    sys.exit()

file_path = os.path.join(DATA_DIR, available_files[0])

def load_data(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    elif path.endswith(".xlsx"):
        df = pd.read_excel(path)
    else:
        print("Unsupported file format.")
        return pd.DataFrame()
    
    df.columns = df.columns.str.strip()
    
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
        df = df.dropna(subset=['Date'])
    
    return df

df = load_data(file_path)

if df.empty:
    print("No usable data found in the file.")
    sys.exit()

def download_effect(message):
    print(f"Downloading {message}:", end=" ", flush=True)
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print(" completed")

success = False

# Total Revenue Summary
if {'Revenue', 'Date'}.issubset(df.columns):
    total_revenue = df['Revenue'].sum()
    time.sleep(0.5)
    print(f"Total Revenue: {total_revenue}")

# Monthly Revenue
if {'Revenue', 'Date'}.issubset(df.columns):
    monthly = df.groupby('Month')['Revenue'].sum().reset_index()
    fig = px.line(monthly, x='Month', y='Revenue', title='Monthly Revenue',
                  color_discrete_sequence=COLOR_PALETTE)
    fig.write_image(os.path.join(REPORTS_DIR, "monthly_revenue.png"))
    download_effect("Monthly Revenue")
    success = True

# Sales by Region
if {'Revenue', 'Region'}.issubset(df.columns):
    region_sales = df.groupby('Region')['Revenue'].sum().reset_index()
    fig = px.pie(region_sales, names='Region', values='Revenue',
                 title='Sales by Region',
                 color_discrete_sequence=COLOR_PALETTE)
    fig.write_image(os.path.join(REPORTS_DIR, "sales_by_region.png"))
    download_effect("Sales by Region")
    success = True

# Revenue by Category
if {'Revenue', 'Category'}.issubset(df.columns):
    category_data = df.groupby('Category')['Revenue'].sum().reset_index()
    fig = px.bar(category_data, x='Category', y='Revenue',
                 title='Revenue by Category',
                 color='Category', color_discrete_sequence=COLOR_PALETTE)
    fig.write_image(os.path.join(REPORTS_DIR, "revenue_by_category.png"))
    download_effect("Revenue by Category")
    success = True

# Top 5 Products by Revenue
if {'Revenue', 'Product'}.issubset(df.columns):
    top_products = df.groupby('Product')['Revenue'].sum().nlargest(5).reset_index()
    fig = px.bar(top_products, x='Revenue', y='Product', orientation='h',
                 title='Top Products by Revenue', color='Product',
                 color_discrete_sequence=COLOR_PALETTE)
    fig.write_image(os.path.join(REPORTS_DIR, "top_products.png"))
    download_effect("Top Products by Revenue")
    success = True

# Quantity Sold by Category
if {'Quantity', 'Category'}.issubset(df.columns):
    category_qty = df.groupby('Category')['Quantity'].sum().reset_index()
    fig = px.bar(category_qty, x='Category', y='Quantity',
                 title='Units Sold per Category',
                 color='Category', color_discrete_sequence=COLOR_PALETTE)
    fig.write_image(os.path.join(REPORTS_DIR, "quantity_by_category.png"))
    download_effect("Quantity Sold by Category")
    success = True

# Top 5 Products by Quantity Sold
if {'Quantity', 'Product'}.issubset(df.columns):
    quantity_data = df.groupby('Product')['Quantity'].sum().nlargest(5).reset_index()
    fig = px.bar(quantity_data, x='Quantity', y='Product', orientation='h',
                 title='Top 5 Products by Quantity',
                 color='Product', color_discrete_sequence=COLOR_PALETTE)
    fig.write_image(os.path.join(REPORTS_DIR, "top_products_quantity.png"))
    download_effect("Top Products by Quantity Sold")
    success = True

# Final check
if not success:
    print("No analytics could be exported. Please make sure your file contains at least one of the following combinations:")
    print("• Revenue + Date")
    print("• Revenue + Product")
    print("• Revenue + Region")
    print("• Revenue + Category")
    print("• Quantity + Product")
    print("• Quantity + Category")
else:
    time.sleep(1)
    print("\nCheck the reports/ depository")

    # If the placeholder file exists and something was exported, delete it
    if placeholder_exists:
        try:
            os.remove(PLACEHOLDER_FILE)
        except Exception as e:
            pass
