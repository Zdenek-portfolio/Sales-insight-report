import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Config
DATA_DIR = 'data'
OUTPUT_DIR = 'reports/'

st.set_page_config(page_title="SalesInsight Dashboard", layout="centered")
st.title("SalesInsight Report Generator")

# Functions
def load_data_from_path(file_path):
    if file_path.suffix == '.xlsx':
        return pd.read_excel(file_path)
    elif file_path.suffix == '.csv':
        return pd.read_csv(file_path)
    else:
        st.error("Unsupported file format: %s" % file_path.suffix)
        return None

def clean_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Quantity'] * df['Unit Price']
    return df

def total_revenue(df):
    return df['Revenue'].sum()

def top_products(df, n=5):
    return df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(n)

def monthly_trends(df):
    return df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum()

def plot_monthly_trends(trends):
    fig, ax = plt.subplots(figsize=(10, 4))
    trends.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Monthly Revenue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue')
    ax.grid(True)
    st.pyplot(fig)

def plot_top_products(top):
    fig, ax = plt.subplots(figsize=(8, 4))
    top.plot(kind='barh', ax=ax, color='salmon')
    ax.set_title('Top Selling Products')
    ax.set_xlabel('Revenue')
    ax.set_ylabel('Product')
    ax.invert_yaxis()
    st.pyplot(fig)

def save_plot(fig, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig.savefig(os.path.join(OUTPUT_DIR, filename), bbox_inches='tight')

# File selection: upload or select existing
uploaded_file = st.file_uploader("Upload your sales data file", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    st.success(f"Loaded uploaded file: {uploaded_file.name}")
else:
    files = list(Path(DATA_DIR).glob('*.xlsx')) + list(Path(DATA_DIR).glob('*.csv'))
    if files:
        file_choice = st.selectbox("Select a file from data folder:", [f.name for f in files])
        df = load_data_from_path(Path(DATA_DIR) / file_choice)
        st.success(f"Loaded file: {file_choice}")
    else:
        st.error(f"No data files found in '{DATA_DIR}' folder.")
        st.stop()

# Clean and analyze
if df is not None:
    df = clean_data(df)

    # Display metrics
    st.subheader("Total Revenue")
    st.metric("Total Revenue", f"${total_revenue(df):,.2f}")

    # Plots
    st.subheader("Monthly Revenue Trend")
    trends = monthly_trends(df)
    plot_monthly_trends(trends)

    st.subheader("Top 5 Products")
    top = top_products(df)
    plot_top_products(top)

    # Save reports
    try:
        plot_monthly_trends(trends)
        plot_top_products(top)
        st.success(f"Reports saved to '{OUTPUT_DIR}' folder.")
    except Exception:
        st.warning("Could not save report images.")
