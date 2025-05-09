
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_PATH = 'data/sales_data.xlsx'
OUTPUT_DIR = 'reports/'

st.set_page_config(page_title="SalesInsight Dashboard", layout="centered")

st.title("SalesInsight Report Generator")

def load_data(path):
    try:
        df = pd.read_excel(path)
    except Exception:
        df = pd.read_csv(path)
    return df

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

# App Logic
if os.path.exists(DATA_PATH):
    df = load_data(DATA_PATH)
    df = clean_data(df)

    st.success("Data loaded successfully!")

    st.subheader("Total Revenue")
    st.metric("Total Revenue", f"${total_revenue(df):,.2f}")

    st.subheader("Monthly Revenue Trend")
    plot_monthly_trends(monthly_trends(df))

    st.subheader("Top 5 Products")
    plot_top_products(top_products(df))

else:
    st.error("sales_data.xlsx not found in /data folder.")
