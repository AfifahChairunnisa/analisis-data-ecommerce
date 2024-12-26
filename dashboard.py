import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide", page_icon="📊")

<<<<<<< HEAD
# Header
=======
# Header dengan Hiasan
>>>>>>> 3db0023 (Initial commit)
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

<<<<<<< HEAD
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
=======
# Gabungkan data pelanggan untuk menambahkan lokasi
orders_data = pd.merge(orders_data, customers_data[['customer_id', 'customer_state']], on='customer_id', how='left')

# Gabungkan data ulasan untuk menambahkan skor ulasan
orders_data = pd.merge(orders_data, order_reviews_data[['order_id', 'review_score']], on='order_id', how='left')

# Konversi kolom tanggal
orders_data['order_purchase_timestamp'] = pd.to_datetime(orders_data['order_purchase_timestamp'], errors='coerce')
orders_data['order_delivered_customer_date'] = pd.to_datetime(orders_data['order_delivered_customer_date'], errors='coerce')
orders_data['order_estimated_delivery_date'] = pd.to_datetime(orders_data['order_estimated_delivery_date'], errors='coerce')
>>>>>>> 3db0023 (Initial commit)

# Sidebar
st.sidebar.title("Pilih Analisis")
analysis_type = st.sidebar.selectbox(
    "Pilih Analisis:",
<<<<<<< HEAD
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
=======
    ["Produk Terlaris", "Pendapatan Penjualan"]
)

# Fitur 1: Analisis Produk Terlaris
if analysis_type == "Produk Terlaris":
    st.subheader("Produk Terlaris📈")
    
    # Pilih tahun untuk analisis
    years = sorted(orders_data['order_purchase_timestamp'].dt.year.dropna().unique(), reverse=True)
    year = st.sidebar.selectbox("Pilih Tahun", options=years)    

    # Pilih filter tambahan (lokasi atau ulasan)
    filter_type = st.sidebar.selectbox("Pilih Filter:", ["Semua", "Lokasi", "Ulasan"])
    
    # Gabungkan data untuk analisis
    orders_data['order_purchase_year'] = orders_data['order_purchase_timestamp'].dt.year
    merged_data = pd.merge(order_items_data, orders_data[['order_id', 'order_purchase_year', 'customer_state', 'review_score']], on='order_id', how='inner')
    merged_data = pd.merge(merged_data, products_data[['product_id', 'product_category_name']], on='product_id', how='inner')
    merged_data = pd.merge(merged_data, product_category_data, on='product_category_name', how='left')

    # Filter berdasarkan tahun
    filtered_data = merged_data[merged_data['order_purchase_year'] == year]

    # Filter tambahan: Lokasi
    if filter_type == "Lokasi":
        state_options = ["Semua"] + list(filtered_data['customer_state'].dropna().unique())
        selected_state = st.sidebar.selectbox("Pilih Lokasi (Negara Bagian):", options=state_options)
        
        # Jika "Semua" tidak dipilih, filter berdasarkan lokasi
        if selected_state != "Semua":
            filtered_data = filtered_data[filtered_data['customer_state'] == selected_state]

    # Filter tambahan: Ulasan
    if filter_type == "Ulasan":
        min_review_options = [1, 2, 3, 4, 5]
        min_review = st.sidebar.selectbox("Pilih Minimum Skor Ulasan:", options=["Semua"] + min_review_options)
        
        # Jika "Semua" tidak dipilih, filter berdasarkan ulasan
        if min_review != "Semua":
            filtered_data = filtered_data[filtered_data['review_score'] >= int(min_review)]
    
    # Hitung produk terlaris
    top_products = filtered_data.groupby('product_category_name_english')['order_id'].count().reset_index()
    top_products = top_products.rename(columns={"order_id": "sales_count"}).sort_values('sales_count', ascending=False)
    
    # Tampilkan data dan visualisasi
    st.write(f"**Produk Terlaris Tahun {year} ({filter_type}):**")
    st.dataframe(top_products.head(10))
    
    fig = px.bar(
        top_products.head(10),
        x='product_category_name_english',
        y='sales_count',
        title=f"Produk Terlaris Tahun {year} ({filter_type})",
        labels={'product_category_name_english': 'Kategori Produk', 'sales_count': 'Jumlah Penjualan'}
    )
    st.plotly_chart(fig)

# Fitur 2: Analisis Tren Pendapatan Penjualan
elif analysis_type == "Pendapatan Penjualan":
    st.subheader("Tren Pendapatan Penjualan📊")
    
    # Tambahkan kolom pendapatan ke dataset order_items_data
    order_items_data['revenue'] = order_items_data['price']

    # Gabungkan dengan data pesanan untuk mendapatkan tanggal pembelian
    revenue_data = pd.merge(order_items_data, orders_data[['order_id', 'order_purchase_timestamp', 'customer_state']], on='order_id', how='left')
    revenue_data = pd.merge(revenue_data, products_data[['product_id', 'product_category_name']], on='product_id', how='left')
    revenue_data = pd.merge(revenue_data, product_category_data, on='product_category_name', how='left')

    # Konversi kolom tanggal pembelian ke datetime
    revenue_data['order_purchase_timestamp'] = pd.to_datetime(revenue_data['order_purchase_timestamp'])

    # Sub-analisis dropdown
    sub_analysis = st.sidebar.selectbox("Pilih Sub-Analisis:", [
        "Pendapatan Total", 
        "Pendapatan Berdasarkan Lokasi", 
        "Pendapatan Berdasarkan Kategori Produk"
    ])

    # Sub-Analisis 1: Pendapatan Total
    if sub_analysis == "Pendapatan Total":
        # Pilih periode tren (bulanan atau tahunan)
        trend_type = st.sidebar.selectbox("Pilih Periode Tren:", ["Bulanan", "Tahunan"])

        # Agregasi data berdasarkan periode
        if trend_type == "Bulanan":
            revenue_data['period'] = revenue_data['order_purchase_timestamp'].dt.to_period('M').astype(str)
        elif trend_type == "Tahunan":
            revenue_data['period'] = revenue_data['order_purchase_timestamp'].dt.to_period('Y').astype(str)

        # Hitung total pendapatan per periode
        revenue_trend = revenue_data.groupby('period')['revenue'].sum().reset_index()
        revenue_trend = revenue_trend.rename(columns={'period': 'Periode', 'revenue': 'Pendapatan Total'})

        # Tampilkan data
        st.write(f"**Tren Pendapatan Penjualan ({trend_type}):**")
        st.dataframe(revenue_trend)

        # Visualisasi tren pendapatan
        fig = px.line(
            revenue_trend,
            x='Periode',
            y='Pendapatan Total',
            title=f"Tren Pendapatan Penjualan ({trend_type})",
            labels={'Periode': 'Periode', 'Pendapatan Total': 'Pendapatan Total (IDR)'}
        )
        st.plotly_chart(fig)

    # Sub-Analisis 2: Pendapatan Berdasarkan Lokasi
    elif sub_analysis == "Pendapatan Berdasarkan Lokasi":
        # Agregasi pendapatan berdasarkan lokasi
        revenue_by_location = revenue_data.groupby('customer_state')['revenue'].sum().reset_index()
        revenue_by_location = revenue_by_location.rename(columns={'customer_state': 'Lokasi', 'revenue': 'Pendapatan Total'})
        revenue_by_location = revenue_by_location.sort_values('Pendapatan Total', ascending=False)

        # Tampilkan data
        st.write("**Pendapatan Berdasarkan Lokasi:**")
        st.dataframe(revenue_by_location)

        # Visualisasi pendapatan berdasarkan lokasi
        fig = px.bar(
            revenue_by_location.head(10),
            x='Lokasi',
            y='Pendapatan Total',
            title="Pendapatan Berdasarkan Lokasi (Top 10)",
            labels={'Lokasi': 'Negara Bagian', 'Pendapatan Total': 'Pendapatan Total (IDR)'}
        )
        st.plotly_chart(fig)

    # Sub-Analisis 3: Pendapatan Berdasarkan Kategori Produk
    elif sub_analysis == "Pendapatan Berdasarkan Kategori Produk":
        # Agregasi pendapatan berdasarkan kategori produk
        revenue_by_category = revenue_data.groupby('product_category_name_english')['revenue'].sum().reset_index()
        revenue_by_category = revenue_by_category.rename(columns={'product_category_name_english': 'Kategori Produk', 'revenue': 'Pendapatan Total'})
        revenue_by_category = revenue_by_category.sort_values('Pendapatan Total', ascending=False)

        # Tampilkan data
        st.write("**Pendapatan Berdasarkan Kategori Produk:**")
        st.dataframe(revenue_by_category)

        # Visualisasi pendapatan berdasarkan kategori produk
        fig = px.bar(
            revenue_by_category.head(10),
            x='Kategori Produk',
            y='Pendapatan Total',
            title="Pendapatan Berdasarkan Kategori Produk (Top 10)",
            labels={'Kategori Produk': 'Kategori', 'Pendapatan Total': 'Pendapatan Total (IDR)'}
        )
        st.plotly_chart(fig)

>>>>>>> 3db0023 (Initial commit)
