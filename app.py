import streamlit as st
import pandas as pd
import plotly.express as px

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="BMW Worldwide Sales 2010–2024",
    layout="wide"
)

st.title("BMW Worldwide Sales (2010–2024)")
st.caption("Visualisasi interaktif penjualan BMW berdasarkan tahun, region, dan model.")


# LOAD DATA
@st.cache_data
def load_data_from_path(path: str):
    df = pd.read_csv(path)
    return df

st.sidebar.header("🔧 Pengaturan Data")

# Ganti ini kalau nama file di laptop kamu beda
default_path = "BMW_Sales_Data_2010_2024"

use_uploaded = st.sidebar.checkbox(
    "Gunakan file CSV upload (bukan file lokal)",
    value=False
)

df = None

if use_uploaded:
    uploaded_file = st.sidebar.file_uploader("Upload file CSV BMW", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
else:
    try:
        df = load_data_from_path(default_path)
        st.sidebar.success(f"Berhasil load data dari `{default_path}`")
    except Exception as e:
        st.sidebar.error(f"Gagal load `{default_path}`: {e}")
        st.sidebar.info("Coba centang opsi 'Gunakan file CSV upload' dan upload manual.")

if df is None:
    st.stop()

EXPECTED_COLS = [
    "Model", "Year", "Region", "Color", "Fuel_Type", "Transmission",
    "Engine_Size_L", "Mileage_KM", "Price_USD", "Sales_Volume",
    "Sales_Classification"
]

missing_cols = [c for c in EXPECTED_COLS if c not in df.columns]
if missing_cols:
    st.error(f"Kolom berikut tidak ditemukan di dataset: {missing_cols}")
    st.write("Kolom yang ada di dataset:", list(df.columns))
    st.stop()

# Tambahkan kolom Revenue (perkiraan) = Price * Sales_Volume
df["Revenue_USD"] = df["Price_USD"] * df["Sales_Volume"]

# TAMPILKAN SAMPLE DATA
with st.expander("Lihat sample data mentah"):
    st.dataframe(df.head(20), use_container_width=True)


# SIDEBAR FILTER
st.sidebar.header(" Filter Data")

# Tahun
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider(
    "Range Tahun",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1
)

# Region
region_options = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=region_options,
    default=region_options  # default: semua region
)

# Model
model_options = sorted(df["Model"].unique())
selected_models = st.sidebar.multiselect(
    "Model",
    options=model_options,
    default=[]
)

# Fuel Type
fuel_options = sorted(df["Fuel_Type"].unique())
selected_fuels = st.sidebar.multiselect(
    "Fuel Type",
    options=fuel_options,
    default=[]
)

# Transmission
trans_options = sorted(df["Transmission"].unique())
selected_trans = st.sidebar.multiselect(
    "Transmission",
    options=trans_options,
    default=[]
)

# Color
color_options = sorted(df["Color"].unique())
selected_colors = st.sidebar.multiselect(
    "Color",
    options=color_options,
    default=[]
)

# Range harga
price_min, price_max = int(df["Price_USD"].min()), int(df["Price_USD"].max())
price_range = st.sidebar.slider(
    "Range Harga (USD)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    step=1000
)

# Range mileage
mileage_min, mileage_max = int(df["Mileage_KM"].min()), int(df["Mileage_KM"].max())
mileage_range = st.sidebar.slider(
    "Range Mileage (KM)",
    min_value=mileage_min,
    max_value=mileage_max,
    value=(mileage_min, mileage_max),
    step=5000
)


# APLIKASI FILTER
filtered_df = df.copy()

# Tahun
filtered_df = filtered_df[
    (filtered_df["Year"] >= year_range[0]) &
    (filtered_df["Year"] <= year_range[1])
]

# Region
if selected_regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]

# Model
if selected_models:
    filtered_df = filtered_df[filtered_df["Model"].isin(selected_models)]

# Fuel Type
if selected_fuels:
    filtered_df = filtered_df[filtered_df["Fuel_Type"].isin(selected_fuels)]

# Transmission
if selected_trans:
    filtered_df = filtered_df[filtered_df["Transmission"].isin(selected_trans)]

# Color
if selected_colors:
    filtered_df = filtered_df[filtered_df["Color"].isin(selected_colors)]

# Harga
filtered_df = filtered_df[
    (filtered_df["Price_USD"] >= price_range[0]) &
    (filtered_df["Price_USD"] <= price_range[1])
]

# Mileage
filtered_df = filtered_df[
    (filtered_df["Mileage_KM"] >= mileage_range[0]) &
    (filtered_df["Mileage_KM"] <= mileage_range[1])
]

# Kalau setelah filter kosong
if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan filter. Coba longgarkan filternya.")
    st.stop()


# METRIK RINGKASAN
st.subheader("Ringkasan Data (Setelah Filter)")

total_units = filtered_df["Sales_Volume"].sum()
total_revenue = filtered_df["Revenue_USD"].sum()
total_rows = len(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Unit Terjual", f"{int(total_units):,}")
col2.metric("Estimasi Total Revenue (USD)", f"{int(total_revenue):,}")
col3.metric("Jumlah Baris Data", f"{total_rows:,}")


# VISUALISASI
tab1, tab2, tab3, tab4 = st.tabs([
    "Trend per Tahun",
    "Region per Tahun",
    "Top Model Terlaris",
    "Price vs Mileage"
])

# 1. Trend penjualan per tahun
with tab1:
    st.markdown("### Trend Penjualan (Sales_Volume) per Tahun")

    trend_year = (
        filtered_df
        .groupby("Year", as_index=False)["Sales_Volume"]
        .sum()
        .sort_values("Year")
    )

    fig_trend = px.line(
        trend_year,
        x="Year",
        y="Sales_Volume",
        markers=True,
        labels={"Year": "Tahun", "Sales_Volume": "Sales Volume"},
        title="Total Sales Volume per Tahun"
    )
    fig_trend.update_layout(hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

# 2. Penjualan per region per tahun
with tab2:
    st.markdown("### Penjualan per Region per Tahun")

    region_year = (
        filtered_df
        .groupby(["Year", "Region"], as_index=False)["Sales_Volume"]
        .sum()
    )

    fig_region = px.bar(
        region_year,
        x="Year",
        y="Sales_Volume",
        color="Region",
        barmode="group",
        labels={"Year": "Tahun", "Sales_Volume": "Sales Volume", "Region": "Region"},
        title="Sales Volume per Region per Tahun"
    )
    st.plotly_chart(fig_region, use_container_width=True)

# 3. Top N model terlaris
with tab3:
    st.markdown("### Top N Model Terlaris")

    top_n = st.slider(
        "Pilih Top N",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

    model_sales = (
        filtered_df
        .groupby("Model", as_index=False)["Sales_Volume"]
        .sum()
        .sort_values("Sales_Volume", ascending=False)
        .head(top_n)
    )

    fig_model = px.bar(
        model_sales,
        x="Model",
        y="Sales_Volume",
        labels={"Model": "Model", "Sales_Volume": "Sales Volume"},
        title=f"Top {top_n} Model Terlaris (berdasarkan filter saat ini)"
    )
    fig_model.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_model, use_container_width=True)

    with st.expander("Lihat tabel Top Model"):
        st.dataframe(model_sales, use_container_width=True)

# 4. Scatter Price vs Mileage
with tab4:
    st.markdown("### Price vs Mileage (per Model)")

    fig_scatter = px.scatter(
        filtered_df,
        x="Mileage_KM",
        y="Price_USD",
        color="Fuel_Type",
        size="Sales_Volume",
        hover_data=["Model", "Region", "Transmission"],
        labels={
            "Mileage_KM": "Mileage (KM)",
            "Price_USD": "Price (USD)",
            "Fuel_Type": "Fuel Type"
        },
        title="Hubungan Mileage vs Price (warna = Fuel Type, ukuran = Sales Volume)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# TABEL DATA AKHIR

st.markdown("### Data Detail (Setelah Filter)")
st.dataframe(filtered_df, use_container_width=True)
