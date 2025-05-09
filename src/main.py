import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Config
DATA_DIR = 'data'
OUTPUT_DIR = 'reports/'

# Load data
def load_data():
    files = list(Path(DATA_DIR).glob('*.xlsx')) + list(Path(DATA_DIR).glob('*.csv'))
    if not files:
        raise FileNotFoundError("No .xlsx or .csv file found in the 'data' folder.")
    
    file = files[0]  # vezmeme první nalezený soubor
    print(f"Loaded file: {file.name}")
    
    if file.suffix == '.xlsx':
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)
    return df

# Preprocess data
def clean_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Quantity'] * df['Unit Price']
    return df

# Analyze
def total_revenue(df):
    return df['Revenue'].sum()

def top_products(df, n=5):
    return df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(n)

def monthly_trends(df):
    return df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum()

# Visualizations
def save_plot(fig, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig.savefig(os.path.join(OUTPUT_DIR, filename), bbox_inches='tight')

def plot_monthly_trends(trends):
    fig, ax = plt.subplots(figsize=(10, 6))
    trends.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Monthly Revenue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue')
    ax.grid(True)
    save_plot(fig, 'monthly_revenue.png')
    plt.close()

def plot_top_products(top):
    fig, ax = plt.subplots(figsize=(8, 5))
    top.plot(kind='barh', ax=ax, color='salmon')
    ax.set_title('Top Selling Products')
    ax.set_xlabel('Revenue')
    ax.set_ylabel('Product')
    ax.invert_yaxis()
    save_plot(fig, 'top_products.png')
    plt.close()

# Main Logic
def main():
    df = load_data()
    df = clean_data(df)

    revenue = total_revenue(df)
    top = top_products(df)
    trends = monthly_trends(df)

    print(f"Total revenue: ${revenue:,.2f}")
    print("\nTop products:\n", top)

    plot_monthly_trends(trends)
    plot_top_products(top)

    print(f"\nReports saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
