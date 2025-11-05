# BMW Global Sales Dashboard (2010–2024)

Proyek ini adalah aplikasi **visualisasi data interaktif** berbasis **Streamlit** yang menampilkan data penjualan BMW di berbagai region dunia dari tahun **2010 hingga 2024**.

Demo App : https://bmw-worldwide-sales-visualization-app-t66umepaoupbf8fd3hspyl.streamlit.app/

---

## ✨ Fitur Utama

- **Filter interaktif**:
  - Tahun (range slider)
  - Region
  - Model
  - Fuel Type
  - Transmission
  - Color
  - Range harga (USD)
  - Range mileage (KM)

- **Metrik ringkasan**:
  - Total unit terjual (Sales_Volume)
  - Estimasi total revenue (Price_USD × Sales_Volume)
  - Jumlah baris data setelah filter

- **Visualisasi interaktif**:
  1. **Trend penjualan per tahun**  
     Line chart total Sales_Volume per Year.
  2. **Penjualan per region per tahun**  
     Bar chart grouped berdasar Year dan Region.
  3. **Top N model terlaris**  
     Bar chart model dengan Sales_Volume tertinggi.
  4. **Scatter Price vs Mileage**  
     Hubungan harga dan mileage, dikodekan dengan Fuel_Type dan ukuran bubble = Sales_Volume.

- **Data detail**:  
  Tabel interaktif (sortable & scrollable) untuk melihat data setelah filter.

---

## 📂 Dataset

Proyek ini menggunakan dataset:

**BMW sales data (2010–2024)**  
File default yang digunakan di aplikasi:  
`BMW sales data (2010-2024) (1).csv`

Struktur kolom utama yang digunakan:

- `Model`
- `Year`
- `Region`
- `Color`
- `Fuel_Type`
- `Transmission`
- `Engine_Size_L`
- `Mileage_KM`
- `Price_USD`
- `Sales_Volume`
- `Sales_Classification`

Tambahan kolom yang dihitung di aplikasi:
- `Revenue_USD` = `Price_USD` × `Sales_Volume`

> **Catatan:**  
> Pastikan nama kolom di CSV kamu sesuai dengan daftar di atas. Jika berbeda, kamu bisa menyesuaikan bagian kode yang menangani kolom-kolom tersebut di `app.py`.

---

## 🛠️ Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

---

## ⚙️ Instalasi & Menjalankan Aplikasi

1. **Clone repo / salin project ke folder lokal**

   ```bash
   git clone <url-repo-ini>  # atau copy file app.py & CSV ke satu folder
   cd <nama-folder-project>
