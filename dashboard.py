import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide", page_icon="📊")

# Header
st.markdown("""
# **Dashboard Analisis E-Commerce**
---
""")

# Fungsi untuk memuat dataset
@st.cache_data
def load_data():
    try:
        orders_data = pd.read_csv('E-Commerce Public Dataset/orders_dataset.csv')
        order_items_data = pd.read_csv('E-Commerce Public Dataset/order_items_dataset.csv')
        products_data = pd.read_csv('E-Commerce Public Dataset/products_dataset.csv')
        product_category_data = pd.read_csv('E-Commerce Public Dataset/product_category_name_translation.csv')
        customers_data = pd.read_csv('E-Commerce Public Dataset/customers_dataset.csv')
        order_reviews_data = pd.read_csv('E-Commerce Public Dataset/order_reviews_dataset.csv')
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None, None
    return orders_data, order_items_data, products_data, product_category_data, customers_data, order_reviews_data

# Memuat data
orders_data, order_items_data, products_data, product_category_data, customers_data, order_reviews_data = load_data()
if orders_data is None:
    st.stop()

# Gabungkan data untuk menambahkan kolom customer_state
orders_data = pd.merge(
    orders_data,
    customers_data[['customer_id', 'customer_state']],
    on='customer_id',
    how='left'
)

# Gabungkan data lainnya untuk analisis
orders_data['order_purchase_year'] = pd.to_datetime(orders_data['order_purchase_timestamp']).dt.year
orders_data['order_purchase_year'] = orders_data['order_purchase_year'].astype(int)  # Pastikan tahun sebagai integer

merged_data = pd.merge(
    order_items_data,
    orders_data[['order_id', 'order_purchase_year', 'customer_state']],
    on='order_id',
    how='inner'
)
merged_data = pd.merge(
    merged_data,
    products_data[['product_id', 'product_category_name']],
    on='product_id',
    how='inner'
)
merged_data = pd.merge(
    merged_data,
    product_category_data,
    on='product_category_name',
    how='left'
)
merged_data = pd.merge(
    merged_data,
    order_reviews_data[['order_id', 'review_score']],
    on='order_id',
    how='left'
)

# Sidebar
st.sidebar.title("Pilih Analisis")
analysis_type = st.sidebar.selectbox(
    "Pilih Analisis:",
    ["Produk Terlaris", "Tren Pendapatan"]
)

# Analisis Produk Terlaris
if analysis_type == "Produk Terlaris":
    st.subheader("Produk Paling Laris📈")
    
    # Pilih filter
    filter_type = st.sidebar.selectbox(
        "Pilih Analisis Produk Terlaris Berdasarkan:",
        ["Tahun", "Lokasi"]
    )

    # Produk Terlaris Berdasarkan Tahun
    if filter_type == "Tahun":
        # Pilih tahun untuk analisis
        years = sorted(merged_data['order_purchase_year'].dropna().unique())
        selected_year = st.sidebar.selectbox("Pilih Tahun:", ["Semua"] + years)
        
        if selected_year != "Semua":
            filtered_data = merged_data[merged_data['order_purchase_year'] == selected_year]
        else:
            filtered_data = merged_data
        
        # Hitung produk terlaris
        top_products = (
            filtered_data
            .groupby('product_category_name_english')['order_id']
            .count()
            .reset_index()
            .rename(columns={'order_id': 'Jumlah Penjualan'})
            .sort_values('Jumlah Penjualan', ascending=False)
        )
        
        # Tampilkan hasil
        st.write(f"**10 Produk Terlaris Tahun {selected_year if selected_year != 'Semua' else '(Semua Tahun)'}:**")
        st.dataframe(top_products.head(10))

        # Visualisasi
        fig = px.bar(
            top_products.head(10),
            x='product_category_name_english',
            y='Jumlah Penjualan',
            title=f"10 Produk Terlaris Tahun {selected_year if selected_year != 'Semua' else '(Semua Tahun)'}",
            labels={'product_category_name_english': 'Kategori Produk', 'Jumlah Penjualan': 'Jumlah Penjualan'}
        )
        fig.update_layout(xaxis=dict(type='category'))  # Memastikan tahun sebagai kategori
        st.plotly_chart(fig)

    # Produk Terlaris Berdasarkan Lokasi
    elif filter_type == "Lokasi":
        # Pilih lokasi untuk analisis
        locations = ["Semua"] + list(merged_data['customer_state'].dropna().unique())
        selected_location = st.sidebar.selectbox("Pilih Lokasi:", locations)
        
        if selected_location != "Semua":
            filtered_data = merged_data[merged_data['customer_state'] == selected_location]
        else:
            filtered_data = merged_data
        
        # Hitung produk terlaris berdasarkan lokasi
        top_products_location = (
            filtered_data
            .groupby('product_category_name_english')['order_id']
            .count()
            .reset_index()
            .rename(columns={'order_id': 'Jumlah Penjualan'})
            .sort_values('Jumlah Penjualan', ascending=False)
        )
        
        # Tampilkan hasil
        st.write(f"**Produk Terlaris di {selected_location if selected_location != 'Semua' else '(Semua Lokasi)'}:**")
        st.dataframe(top_products_location.head(10))

        # Visualisasi
        fig = px.bar(
            top_products_location.head(10),
            x='product_category_name_english',
            y='Jumlah Penjualan',
            title=f"Produk Terlaris di Lokasi {selected_location if selected_location != 'Semua' else '(Semua Lokasi)'}",
            labels={'product_category_name_english': 'Kategori Produk', 'Jumlah Penjualan': 'Jumlah Penjualan'}
        )
        st.plotly_chart(fig)

# Analisis Tren Pendapatan
elif analysis_type == "Tren Pendapatan":
    st.subheader("Tren Pendapatan📊")
    
    # Tambahkan kolom pendapatan
    merged_data['revenue'] = merged_data['price']

    # Pilih jenis analisis
    revenue_analysis_type = st.sidebar.selectbox("Pilih Analisis:", ["Tahunan", "Kategori", "Lokasi"])

    if revenue_analysis_type == "Tahunan":
        # Pendapatan tahunan
        revenue_by_year = merged_data.groupby('order_purchase_year')['revenue'].sum().reset_index()
        revenue_by_year.columns = ['Tahun', 'Pendapatan']

        # Tampilkan hasil
        revenue_by_year['Tahun'] = revenue_by_year['Tahun'].astype(str)
        st.write("**Pendapatan Tahunan:**")
        st.dataframe(revenue_by_year)

        # Visualisasi
        fig = px.bar(
            revenue_by_year,
            x='Tahun',
            y='Pendapatan',
            title="Pendapatan Tahunan",
            labels={'Pendapatan': 'Pendapatan (IDR)'}
        )
        fig.update_layout(xaxis=dict(type='category'))
        st.plotly_chart(fig)

    elif revenue_analysis_type == "Kategori":
        # Pendapatan berdasarkan kategori
        revenue_by_category = merged_data.groupby('product_category_name_english')['revenue'].sum().reset_index()
        revenue_by_category.columns = ['Kategori Produk', 'Pendapatan']
        revenue_by_category = revenue_by_category.sort_values(by='Pendapatan', ascending=False)

        # Tampilkan hasil
        st.write("**Pendapatan Berdasarkan Kategori Produk:**")
        st.dataframe(revenue_by_category.head(10))

        # Visualisasi
        fig = px.bar(
            revenue_by_category.head(10),
            x='Kategori Produk',
            y='Pendapatan',
            title="Pendapatan Berdasarkan Kategori Produk (Top 10)",
            labels={'Pendapatan': 'Pendapatan (IDR)'}
        )
        st.plotly_chart(fig)

    elif revenue_analysis_type == "Lokasi":
        # Pendapatan berdasarkan lokasi
        revenue_by_location = merged_data.groupby('customer_state')['revenue'].sum().reset_index()
        revenue_by_location.columns = ['Lokasi', 'Pendapatan']
        revenue_by_location = revenue_by_location.sort_values(by='Pendapatan', ascending=False)

        # Tampilkan hasil
        st.write("**Pendapatan Berdasarkan Lokasi:**")
        st.dataframe(revenue_by_location)

        # Visualisasi
        fig = px.bar(
            revenue_by_location.head(10),
            x='Lokasi',
            y='Pendapatan',
            title="Pendapatan Berdasarkan Lokasi (Top 10)",
            labels={'Pendapatan': 'Pendapatan (IDR)'}
        )
        st.plotly_chart(fig)
