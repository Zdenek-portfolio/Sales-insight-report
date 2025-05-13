import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Consistent color palette for all charts
COLOR_PALETTE = px.colors.qualitative.Set2

# Check if reports directory exists
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# Load file from data folder
data_folder = "data"
available_files = [f for f in os.listdir(data_folder) if f.endswith((".csv", ".xlsx"))]
selected_file = st.sidebar.selectbox("Select a sales data file", available_files)
file_path = os.path.join(data_folder, selected_file)

@st.cache_data
def load_data(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    elif path.endswith(".xlsx"):
        df = pd.read_excel(path)
    else:
        st.error("Unsupported file format.")
        return pd.DataFrame()
    
    df.columns = df.columns.str.strip()
    
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    
    df = df.dropna(subset=['Date']) if 'Date' in df.columns else df
    return df

df = load_data(file_path)

if df.empty:
    st.warning("No data loaded.")
    st.stop()

st.title("Sales Insight Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filter Data")

if 'Date' in df.columns:
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]

if 'Region' in df.columns:
    regions = df['Region'].dropna().unique().tolist()
    selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)
    df = df[df['Region'].isin(selected_regions)]

# Flags to track which analytics were shown
analytics_displayed = 0

# 1. Total Revenue Summary
if 'Revenue' in df.columns and 'Date' in df.columns:
    total_revenue = df['Revenue'].sum()
    st.subheader("Total Revenue")
    st.info(f"Total Revenue for Selected Period: **${total_revenue:,.2f}**")
    analytics_displayed += 1
    st.markdown("---")

# 2. Monthly Revenue
if 'Revenue' in df.columns and 'Date' in df.columns:
    st.subheader("Monthly Revenue")
    monthly_revenue = df.groupby('Month')['Revenue'].sum().reset_index()
    fig_monthly = px.line(monthly_revenue, x='Month', y='Revenue',
                          title='Monthly Revenue',
                          color_discrete_sequence=COLOR_PALETTE)
    st.plotly_chart(fig_monthly, use_container_width=True)
    analytics_displayed += 1
    st.markdown("---")

# 3. Top 5 Products by Revenue
if 'Revenue' in df.columns and 'Product' in df.columns:
    st.subheader("Top 5 Products by Revenue")
    top_products = df.groupby('Product')['Revenue'].sum().nlargest(5).reset_index()
    fig_top_products = px.bar(top_products, x='Revenue', y='Product', orientation='h',
                              title='Top 5 Products by Revenue',
                              color='Product', color_discrete_sequence=COLOR_PALETTE)
    st.plotly_chart(fig_top_products, use_container_width=True)
    analytics_displayed += 1
    st.markdown("---")

# 4. Sales Distribution by Region
if 'Revenue' in df.columns and 'Region' in df.columns:
    st.subheader("Sales Distribution by Region")
    region_sales = df.groupby('Region')['Revenue'].sum().reset_index()
    fig_region = px.pie(region_sales, names='Region', values='Revenue',
                        title='Sales by Region',
                        color_discrete_sequence=COLOR_PALETTE)
    st.plotly_chart(fig_region, use_container_width=True)
    analytics_displayed += 1
    st.markdown("---")

# 5. Revenue by Category
if 'Revenue' in df.columns and 'Category' in df.columns:
    st.subheader("Revenue by Category")
    category_data = df.groupby('Category')['Revenue'].sum().reset_index()
    fig_category = px.bar(category_data, x='Category', y='Revenue',
                          title='Revenue by Category',
                          color='Category', color_discrete_sequence=COLOR_PALETTE)
    st.plotly_chart(fig_category, use_container_width=True)
    analytics_displayed += 1
    st.markdown("---")

# 6. Top Products by Quantity Sold
if 'Quantity' in df.columns and 'Product' in df.columns:
    st.subheader("Top Products by Quantity Sold")
    quantity_data = df.groupby('Product')['Quantity'].sum().nlargest(5).reset_index()
    fig_quantity = px.bar(quantity_data, x='Quantity', y='Product', orientation='h',
                          title='Top 5 Products by Quantity',
                          color='Product', color_discrete_sequence=COLOR_PALETTE)
    st.plotly_chart(fig_quantity, use_container_width=True)
    analytics_displayed += 1
    st.markdown("---")

# 7. Quantity Sold by Category
if 'Quantity' in df.columns and 'Category' in df.columns:
    st.subheader("Quantity Sold by Category")
    category_qty = df.groupby('Category')['Quantity'].sum().reset_index()
    fig_cat_qty = px.bar(category_qty, x='Category', y='Quantity',
                         title='Units Sold per Category',
                         color='Category', color_discrete_sequence=COLOR_PALETTE)
    st.plotly_chart(fig_cat_qty, use_container_width=True)
    analytics_displayed += 1
    st.markdown("---")

# If nothing was shown
if analytics_displayed == 0:
    st.warning("No analytics could be displayed. Please ensure your file contains at least one of the required columns: Revenue, Date, Product, Region, Category, Quantity.")
    st.markdown("---")

# Footer
st.markdown("Developed by Zdenek-portfolio | Powered by Streamlit")
